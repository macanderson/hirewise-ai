import { Text } from '@radix-ui/themes';
import Link from 'next/link';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-gray-200 bg-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center justify-center space-y-4 md:flex-row md:justify-between md:space-y-0">
          <Text size="2" color="gray">
            © {currentYear} HireWise AI. All rights reserved.
          </Text>
          <div className="flex space-x-6">
            <Link href="/terms" className="text-gray-600 hover:text-gray-900 transition-colors">
              <Text size="2">Terms of Service</Text>
            </Link>
            <Link href="/privacy" className="text-gray-600 hover:text-gray-900 transition-colors">
              <Text size="2">Privacy Policy</Text>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
