'use client';

import { Card, Flex, Heading, Text, Button, Select } from '@radix-ui/themes';
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
    const firstName = formData.get('first_name') as string;
    const lastName = formData.get('last_name') as string;
    const organizationName = formData.get('organization_name') as string;
    const organizationSize = formData.get('organization_size') as string;

    if (!email || !password || !organizationName || !organizationSize) {
      setError('Please fill in all required fields');
      setIsLoading(false);
      return;
    }

    try {
      await AuthManager.signUp({
        email,
        password,
        organization_name: organizationName,
        organization_size: parseInt(organizationSize, 10),
        first_name: firstName || undefined,
        last_name: lastName || undefined,
      });
      router.push('/app/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    
    <Card size="4" style={{ backgroundColor: 'white', width: '100%' }} variant="surface">
      
      <Flex direction="column" gap="4">
        <Heading size="6" align="center">
          <Logo width={250} height={100} className="mb-4 mx-auto" />
          <Text size="5" weight="medium">
            Create an account
          </Text>
        </Heading>

        {error && (
          <Text color="red" size="2" align="center">
            {error}
          </Text>
        )}

        <Form.Root onSubmit={handleSubmit} className="space-y-3">
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
                Please enter a password
              </Text>
            </Form.Message>
          </Form.Field>

          <Form.Field name="first_name">
            <Form.Label>
              <Text size="2" weight="medium">
                First Name
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <input
                type="text"
                name="first_name"
                placeholder="First name (optional)"
                className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </Form.Control>
          </Form.Field>

          <Form.Field name="last_name">
            <Form.Label>
              <Text size="2" weight="medium">
                Last Name
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <input
                type="text"
                name="last_name"
                placeholder="Last name (optional)"
                className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </Form.Control>
          </Form.Field>

          <Form.Field name="organization_name">
            <Form.Label>
              <Text size="2" weight="medium">
                Company Name
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <input
                type="text"
                name="organization_name"
                placeholder="Organization"
                required
                className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </Form.Control>
            <Form.Message match="valueMissing">
              <Text size="1" color="red">
                Company Name is required.
              </Text>
            </Form.Message>
          </Form.Field>

          <Form.Field name="organization_size">
            <Form.Label>
              <Text size="2" weight="medium">
                Company Size
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <Select.Root defaultValue="1" name="organization_size">
                <Select.Trigger className="w-full px-3 py-2 text-base bg-white border rounded-md" />
                <Select.Content>
                  <Select.Item value="1">0-1 Employees</Select.Item>
                  <Select.Item value="2">2-9 Employees</Select.Item>
                  <Select.Item value="3">10-49 Employees</Select.Item>
                  <Select.Item value="4">50-249 Employees</Select.Item>
                  <Select.Item value="5">250+ Employees</Select.Item>
                </Select.Content>
              </Select.Root>
            </Form.Control>
          </Form.Field>

          <Form.Submit asChild>
            <Button
              size="3"
              style={{ width: '100%', padding: '1rem', marginTop: '10px' }}
              disabled={isLoading}
            >
              {isLoading ? 'Registering...' : 'Sign Up'}
            </Button>
          </Form.Submit>
        </Form.Root>
      </Flex>
    </Card>
  );
}
