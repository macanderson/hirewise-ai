import { Button, Text, DropdownMenu, Avatar } from '@radix-ui/themes';
import Link from 'next/link';

interface HeaderProps {
  className?: string;
}

export function Header({ className }: HeaderProps) {
  return (
    <header className={`px-6 py-4 ${className || ''}`}>
      <div className="flex items-center justify-end">
        <DropdownMenu.Root>
          <DropdownMenu.Trigger>
            <Button variant="ghost" size="2">
              <Avatar size="2" src="/placeholder-avatar.jpg" fallback="MA" radius="full" />
            </Button>
          </DropdownMenu.Trigger>
          <DropdownMenu.Content>
            <DropdownMenu.Item>
              <Link href="/settings/profile">
                <Text size="2">Profile</Text>
              </Link>
            </DropdownMenu.Item>
            <DropdownMenu.Item>
              <Link href="/settings">
                <Text size="2">Settings</Text>
              </Link>
            </DropdownMenu.Item>
            <DropdownMenu.Item>
              <Link href="/help">
                <Text size="2">Help</Text>
              </Link>
            </DropdownMenu.Item>
            <DropdownMenu.Separator />
            <DropdownMenu.Item color="red">
              <Text size="2">Sign out</Text>
            </DropdownMenu.Item>
          </DropdownMenu.Content>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}

export default Header;
