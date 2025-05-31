'use client';

import { Card, Flex, Heading, Text, Button } from '@radix-ui/themes';
import * as Form from '@radix-ui/react-form';
import React, { useState } from 'react';
import { AuthManager } from '@/lib/auth';
import { Logo } from '@/components/ui/logo';

export default function ResetPasswordPage() {
  const [requestMessage, setRequestMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleRequest = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    const formData = new FormData(event.currentTarget);
    const email = formData.get('email') as string;
    if (!email) return;

    try {
      await AuthManager.requestPasswordReset(email);
      setRequestMessage('Check your email for reset instructions.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send reset email');
    }
  };

  const handleReset = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    const formData = new FormData(event.currentTarget);
    const token = formData.get('reset_token') as string;
    const password = formData.get('new_password') as string;
    if (!token || !password) return;

    try {
      await AuthManager.resetPassword({ reset_token: token, new_password: password });
      setSuccess('Password reset successfully. You can now log in.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Password reset failed');
    }
  };

  return (
    <Card size="4" style={{ backgroundColor: 'white', width: '100%' }} variant="surface">
      <Flex direction="column" gap="4" className="mt-0">
        <Heading size="6" align="center" mx="0" className="flex flex-col items-center mt-0">
          <Logo width={250} height={100} className="mb-4 mx-auto" />
          <Text size="5" weight="medium">
            Reset Password
          </Text>
        </Heading>

        {error && (
          <Text color="red" size="2" align="center">
            {error}
          </Text>
        )}
        {requestMessage && (
          <Text color="green" size="2" align="center">
            {requestMessage}
          </Text>
        )}
        {success && (
          <Text color="green" size="2" align="center">
            {success}
          </Text>
        )}

        <Form.Root onSubmit={handleRequest} className="space-y-3">
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
          <Form.Submit asChild>
            <Button size="3" style={{ width: '100%', marginTop: '10px' }}>
              Send Reset Email
            </Button>
          </Form.Submit>
        </Form.Root>

        <Form.Root onSubmit={handleReset} className="space-y-3 mt-6">
          <Form.Field name="reset_token">
            <Form.Label>
              <Text size="2" weight="medium">
                Reset Token
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <input
                type="text"
                name="reset_token"
                placeholder="Token"
                required
                className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </Form.Control>
          </Form.Field>
          <Form.Field name="new_password">
            <Form.Label>
              <Text size="2" weight="medium">
                New Password
              </Text>
            </Form.Label>
            <Form.Control asChild>
              <input
                type="password"
                name="new_password"
                placeholder="Enter new password"
                required
                className="w-full px-3 py-2 text-base bg-white border rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </Form.Control>
          </Form.Field>
          <Form.Submit asChild>
            <Button size="3" style={{ width: '100%', marginTop: '10px' }}>
              Reset Password
            </Button>
          </Form.Submit>
        </Form.Root>
      </Flex>
    </Card>
  );
}
