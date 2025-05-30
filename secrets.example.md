# Production Secrets Configuration

Set these secrets using `fly secrets set KEY=value` before deploying to production:

## Required Secrets

```bash
# Database connection
fly secrets set DATABASE_URL="postgresql://user:password@host:5432/dbname"

# Redis for caching and background jobs
fly secrets set REDIS_URL="redis://user:password@host:6379"

# JWT authentication
fly secrets set JWT_SECRET_KEY="your-super-secret-jwt-key-minimum-32-characters-long"

# Error tracking (recommended)
fly secrets set SENTRY_DSN="https://your-sentry-dsn@sentry.io/project-id"
```

## Optional Secrets (based on your features)

```bash
# AI features
fly secrets set OPENAI_API_KEY="sk-your-openai-api-key"

# Payment processing
fly secrets set STRIPE_SECRET_KEY="sk_live_your-stripe-secret-key"
fly secrets set STRIPE_WEBHOOK_SECRET="whsec_your-webhook-secret"

# Email service
fly secrets set SENDGRID_API_KEY="SG.your-sendgrid-api-key"

# File storage
fly secrets set AWS_ACCESS_KEY_ID="your-aws-access-key"
fly secrets set AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
fly secrets set AWS_S3_BUCKET="your-s3-bucket-name"

# OAuth providers
fly secrets set GOOGLE_CLIENT_SECRET="your-google-oauth-secret"
fly secrets set GITHUB_CLIENT_SECRET="your-github-oauth-secret"
```

## Verify Secrets

Check that secrets are set correctly:

```bash
fly secrets list
```

## Security Notes

- Never commit secrets to version control
- Use different secrets for staging and production
- Rotate secrets periodically
- Use Fly's secret management rather than environment variables for sensitive data
