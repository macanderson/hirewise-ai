import { Container } from '@radix-ui/themes';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-white flex flex-col">
      {/* Header with logo */}
      <Container className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-start pt-8 pb-4">
          {/* <Link href="/">
            <Logo width={150} height={50} />
          </Link> */}
        </div>

        {/* Main content area */}
        <div className="flex-1 flex items-center justify-center">
          <div className="max-w-md w-full space-y-8">{children}</div>
        </div>

        {/* Footer */}
        <div className="pb-8 text-center">
          <p className="text-sm text-gray-600">
            © {new Date().getFullYear()} HireWise AI. All rights reserved.
          </p>
        </div>
      </Container>
    </div>
  );
}
