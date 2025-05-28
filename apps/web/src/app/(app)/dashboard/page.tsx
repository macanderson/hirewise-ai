'use client';

import { Box, Container, Heading, Text, Button, Flex } from '@radix-ui/themes';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthManager } from '@/lib/auth';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  tenant_id: string;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const isProduction = process.env.NODE_ENV === 'production';
        if (!AuthManager.isAuthenticated()) {
          if (isProduction) {
            router.push('/login');
            return;
          }
          console.warn('User not authenticated in development mode');
        }

        const userData = await AuthManager.getCurrentUser();
        setUser(userData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load user data');
        // If there's an auth error, redirect to login
        // router.push('/login');
        console.error('Error checking auth:', err);
        setError(err instanceof Error ? err.message : 'Failed to load user data');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = async () => {
    try {
      await AuthManager.logout();
      // AuthManager.logout() already redirects to login
    } catch (err) {
      console.error('Logout error:', err);
      // Force redirect even if logout fails
      router.push('/login');
    }
  };

  if (loading) {
    return (
      <Box className="h-screen grid place-items-center">
        <Text size="4">Loading...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="h-screen grid place-items-center">
        <Container size="1">
          <Flex direction="column" align="center" gap="4">
            <Text size="4" color="red">
              Error: {error}
            </Text>
            <Button onClick={() => router.push('/login')}>Go to Login</Button>
          </Flex>
        </Container>
      </Box>
    );
  }

  return (
    <Box className="min-h-screen p-8">
      <Container size="3">
        <Flex direction="column" gap="6">
          <Flex justify="between" align="center">
            <Heading size="8" as="h1">
              Dashboard
            </Heading>
            <Button variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          </Flex>

          {user && (
            <Box className="p-6 border rounded-lg">
              <Heading size="4" mb="4">
                Welcome back!
              </Heading>
              <Flex direction="column" gap="2">
                <Text size="3">
                  <strong>Email:</strong> {user.email}
                </Text>
                {user.first_name && (
                  <Text size="3">
                    <strong>First Name:</strong> {user.first_name}
                  </Text>
                )}
                {user.last_name && (
                  <Text size="3">
                    <strong>Last Name:</strong> {user.last_name}
                  </Text>
                )}
                <Text size="3">
                  <strong>User ID:</strong> {user.id}
                </Text>
                <Text size="3">
                  <strong>Tenant ID:</strong> {user.tenant_id}
                </Text>
              </Flex>
            </Box>
          )}

          <Box className="p-6 border rounded-lg">
            <Heading size="4" mb="4">
              Font Test
            </Heading>
            <Flex direction="column" gap="3">
              <Heading size="6" as="h2">
                This heading uses Aeonik Sans Semibold
              </Heading>
              <Heading size="4" as="h3">
                Smaller heading also uses Aeonik Sans
              </Heading>
              <Text size="3">
                This body text uses Aeonik Fono Regular. It should be clearly different from the
                headings above and provide excellent readability for longer content.
              </Text>
              <Text size="2" color="gray">
                Smaller text also uses Aeonik Fono for consistency.
              </Text>
            </Flex>
          </Box>
        </Flex>
      </Container>
    </Box>
  );
}
