'use client';

import { Card, Flex, Heading, Text, Button } from '@radix-ui/themes';
import * as Form from '@radix-ui/react-form';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthManager } from '@/lib/auth';
import { Logo } from '@/components/ui/logo';

export default function LoginPage() {
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
    const tenantId = formData.get('tenantId') as string;

    if (!email || !password) {
      setError('Please fill in all required fields');
      setIsLoading(false);
      return;
    }

    try {
      await AuthManager.login(
        { username: email, password }, // FastAPI expects 'username' field
        tenantId || undefined
      );

      // Redirect to dashboard on successful login
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card size="4" style={{ backgroundColor: 'white', width: '100%' }} variant="surface">
      <Flex direction="column" gap="4" className="mt-0">
        <Heading size="6" align="center" mx="0" className="flex flex-col items-center mt-0">
          <Logo width={250} height={100} className="mb-4 mx-auto" />
          <Text size="5" weight="medium">
            Login to your account
          </Text>
        </Heading>

        {error && (
          <Text color="red" size="2" align="center">
            {error}
          </Text>
        )}

        <Form.Root onSubmit={handleSubmit}>
          <Flex direction="column" gap="3">
            <Form.Field name="email">
              <Form.Label>
                <Text size="2" weight="medium">
                  Email
                </Text>
              </Form.Label>
              <Form.Control asChild>
                <input
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  required
                  className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </Form.Control>
              <Form.Message match="valueMissing">
                <Text size="1" color="red">
                  Please enter your email
                </Text>
              </Form.Message>
              <Form.Message match="typeMismatch">
                <Text size="1" color="red">
                  Please enter a valid email
                </Text>
              </Form.Message>
            </Form.Field>

            <Form.Field name="password">
              <Form.Label>
                <Text size="2" weight="medium">
                  Password
                </Text>
              </Form.Label>
              <Form.Control asChild>
                <input
                  type="password"
                  name="password"
                  placeholder="Enter your password"
                  required
                  className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </Form.Control>
              <Form.Message match="valueMissing">
                <Text size="1" color="red">
                  Please enter your password
                </Text>
              </Form.Message>
            </Form.Field>

            <Form.Field name="tenantId">
              <Form.Label>
                <Text size="2" weight="medium">
                  Tenant ID (Optional)
                </Text>
              </Form.Label>
              <Form.Control asChild>
                <input
                  type="text"
                  name="tenantId"
                  placeholder="Enter tenant ID (optional)"
                  className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </Form.Control>
            </Form.Field>

            <Form.Submit asChild>
              <Button size="3" style={{ width: '100%' }} disabled={isLoading}>
                {isLoading ? 'Signing in...' : 'Sign In'}
              </Button>
            </Form.Submit>
          </Flex>
        </Form.Root>
      </Flex>
    </Card>
  );
}
