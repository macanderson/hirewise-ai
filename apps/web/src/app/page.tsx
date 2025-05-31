'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { Button, Card, Flex, Heading } from '@radix-ui/themes';

export default async function Home() {
  const cookieStore = await cookies();
  const isLoggedIn = !!cookieStore.get('token');

  if (isLoggedIn) {
    redirect('/app/dashboard');
  }

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-yellow-50 to-white">
      <Card size="4" style={{ backgroundColor: 'white' }} variant="surface">
        <Flex direction="column" gap="4" align="center">
          <Heading size="6">Welcome to HireWise AI</Heading>
          <Flex gap="3" mt="2">
            <Button asChild size="3">
              <Link href="/login">Login</Link>
            </Button>
            <Button asChild size="3" variant="outline">
              <Link href="/sign-up">Sign Up</Link>
            </Button>
          </Flex>
        </Flex>
      </Card>
    </div>
  );
}
