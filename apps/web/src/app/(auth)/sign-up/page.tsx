'use client';
import { Card, Flex, Heading, Text, Button } from '@radix-ui/themes';
import * as Form from '@radix-ui/react-form';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthManager } from '@/lib/auth';
import { Logo } from '@/components/ui/logo';

export default function SignUpPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    const formData = new FormData(event.currentTarget);
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;

    try {
      await AuthManager.signUp({ email, password });
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign up failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card size="4" style={{ backgroundColor: 'white', width: '100%' }} variant="surface">
      <Flex direction="column" gap="4">
        <Heading size="6" align="center">
          <Logo width={250} height={100} className="mb-4 mx-auto" />
          <Text size="5" weight="medium">Create an account</Text>
        </Heading>

        {error && (
          <Text color="red" size="2" align="center">
            {error}
          </Text>
        )}

        <Form.Root onSubmit={handleSubmit} className="space-y-4">
          <Form.Field name="email">
            <Form.Label>Email</Form.Label>
            <Form.Control asChild>
              <input type="email" name="email" required className="w-full px-3 py-2 border rounded" />
            </Form.Control>
          </Form.Field>
          <Form.Field name="password">
            <Form.Label>Password</Form.Label>
            <Form.Control asChild>
              <input type="password" name="password" required className="w-full px-3 py-2 border rounded" />
            </Form.Control>
          </Form.Field>
          <Form.Submit asChild>
            <Button disabled={isLoading}>{isLoading ? 'Signing up...' : 'Sign Up'}</Button>
          </Form.Submit>
        </Form.Root>
      </Flex>
    </Card>
  );
}
