import { Heading, Button, Text } from '@radix-ui/themes';
import Link from 'next/link';
import { Logo } from './logo';

interface HeaderProps {
  className?: string;
}

export function Header({ className }: HeaderProps) {
  return (
    <header className={`bg-white border-b border-gray-200 px-6 py-4 ${className || ''}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link href="/dashboard">
            <Logo width={100} height={32} />
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="2">
            <Text size="2">Help</Text>
          </Button>
          <Button variant="ghost" size="2">
            <Text size="2">Settings</Text>
          </Button>
          <Button variant="solid" size="2">
            <Text size="2">Profile</Text>
          </Button>
        </div>
      </div>
    </header>
  );
}

export default Header;
