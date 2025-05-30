"""
Auth API Routes
--------------------------------
- /api/v1/auth/sign-up  # POST
- /api/v1/auth/login  # POST
- /api/v1/auth/logout  # POST
- /api/v1/auth/refresh  # POST
- /api/v1/auth/change-password  # POST
- /api/v1/auth/request-password-reset  # POST
- /api/v1/auth/reset-password  # POST
- /api/v1/auth/me  # GET
- /api/v1/auth/update-profile  # PATCH
- /api/v1/auth/confirm-email  # GET

"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, StrEnum
from api.services.auth import AuthService, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize auth service
auth_service = AuthService()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class Token(BaseModel):
    """
    Token model
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data model
    """
    email: Optional[str] = None


class OrganizationSize(StrEnum):
    """
    Organization size options for trial sign-up
    """
    SMALL = "0-1 Employees"
    MEDIUM = "2-9 Employees"
    LARGE = "10-49 Employees"
    ENTERPRISE = "50-249 Employees"
    GIANT = "250+ Employees"


class UserRegister(BaseModel):
    """
    User registration model
    """
    email: EmailStr
    password: str
    organization_name: str
    organization_size: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    """
    User login model
    """
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    """
    Password change model
    """
    current_password: str
    new_password: str


class PasswordResetRequest(BaseModel):
    """
    Password reset request model
    """
    email: EmailStr


class PasswordReset(BaseModel):
    """
    Password reset model
    """
    reset_token: str
    new_password: str


class UserProfileUpdate(BaseModel):
    """
    User profile update model
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    organization_name: Optional[str] = None


class UserResponse(BaseModel):
    """
    User response model
    """
    id: str
    tenant_id: str
    email: str
    person_name: str
    organization_name: str
    organization_size: OrganizationSize


@router.post("/sign-up", response_model=Token)
async def register(data: UserRegister, request: Request):
    """Register a new user"""
    tenant_id = None

    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        # If tenant_id provided, verify it exists

        tenant = await auth_service.prisma.tenant.create(
            data={
                "name": f"{data.organization_name or (data.first_name + ' ' + data.last_name) or data.email} Organization",  # noqa: E501
                "deleted": False
            }
        )
        tenant_id = tenant.id

        # Get role - use CUSTOMER_ADMIN if no tenant_id was provided
        role_type = "CUSTOMER_ADMIN" if not request.headers.get("X-Tenant-Id") else "CUSTOMER_USER"  # noqa: E501
        default_role = await auth_service.prisma.userrole.find_first(
            where={"type": role_type}
        )

        # Register user
        result = await auth_service.register_user(
            email=data.email,
            password=data.password,
            tenant_id=tenant_id,
            first_name=data.first_name,
            last_name=data.last_name,
            role_id=default_role.id if default_role else None
        )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None
):

    # Get client info
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        # Authenticate user
        result = await auth_service.login(
            email=form_data.username,
            password=form_data.password,
            ip_address=ip_address,
            tenant_id=None,
            user_agent=user_agent
        )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.post("/logout")
async def logout(
    request: Request,
    token: str = Depends(oauth2_scheme)
):
    """Logout a user"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        success = await auth_service.logout(token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Logout failed"
            )

        return {"message": "Successfully logged out"}

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token: str = Depends(oauth2_scheme)
):
    """Refresh an access token"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        result = await auth_service.refresh_token(token)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"]
        }

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.post("/change-password")
async def change_password(
    data: PasswordChange,
    current_user=Depends(get_current_user)
):
    """Change user password"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        success = await auth_service.change_password(
            user_id=current_user.id,
            current_password=data.current_password,
            new_password=data.new_password
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid current password"
            )

        return {"message": "Password changed successfully"}

    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.post("/request-password-reset")
async def request_password_reset(
    data: PasswordResetRequest,
    request: Request
):

    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        reset_token = await auth_service.request_password_reset(
            email=data.email,
        )

        # In a real application, you would send this token via email
        # For now, we'll return it in the response (NOT for production!)
        if reset_token:
            # TODO: Send email with reset token
            logger.info(
                f"Password reset token for {data.email}: {reset_token}"
            )
            return {
                "message": "Password reset instructions sent to your email",
                # Remove this in production!
                "reset_token": reset_token
            }
        else:
            # Don't reveal whether the email exists
            return {
                "message": "Password reset instructions sent to your email"
            }

    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        # Don't reveal errors for security
        return {"message": "Password reset instructions sent to your email"}
    finally:
        await auth_service.prisma.disconnect()


@router.post("/reset-password")
async def reset_password(data: PasswordReset):
    """Reset password with reset token"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        success = await auth_service.reset_password(
            reset_token=data.reset_token,
            new_password=data.new_password
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        return {"message": "Password reset successfully"}

    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.patch("/update-profile", response_model=UserResponse)
async def update_profile(
    data: UserProfileUpdate,
    current_user=Depends(get_current_user)
):
    """Update user profile information"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        # If email is being changed, we need to send a confirmation email
        email_confirmation_required = False
        if data.email and data.email != current_user.email:
            email_confirmation_required = True

        result = await auth_service.update_user_profile(
            user_id=current_user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            organization_name=data.organization_name
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile update failed"
            )

        # If email was changed, send confirmation email
        if email_confirmation_required:
            confirmation_token = await auth_service.generate_email_confirmation_token(
                user_id=current_user.id,
                new_email=data.email
            )

            # TODO: Send email confirmation email
            logger.info(
                f"Email confirmation token for {data.email}: {confirmation_token}"
            )

        return UserResponse(
            id=result.id,
            tenant_id=result.tenantId,
            email=result.email,
            person_name=f"{result.firstName or ''} {result.lastName or ''}".strip(),
            organization_name=result.tenant.name if result.tenant else "",
            organization_size=OrganizationSize.SMALL  # Default value, adjust as needed
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.get("/confirm-email")
async def confirm_email(
    token: str,
    email: str
):
    """Confirm email address change using URL parameters"""
    # Connect Prisma
    await auth_service.prisma.connect()

    try:
        success = await auth_service.confirm_email_change(
            confirmation_token=token,
            email=email
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired confirmation token"
            )

        return {"message": "Email confirmed successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Email confirmation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email confirmation failed"
        )
    finally:
        await auth_service.prisma.disconnect()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user=Depends(get_current_user)
):
    """Get current user info"""
    return UserResponse(
        id=current_user.id,
        tenant_id=current_user.tenantId,
        email=current_user.email,
        person_name=f"{current_user.firstName or ''} {current_user.lastName or ''}".strip(),
        organization_name=current_user.tenant.name if current_user.tenant else "",
        organization_size=OrganizationSize.SMALL  # Default value, adjust as needed
    )
