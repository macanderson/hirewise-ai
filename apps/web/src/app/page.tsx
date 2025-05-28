'use server';

import { Box, Container, Heading, Text } from '@radix-ui/themes';
import { cookies } from 'next/headers';
import Image from 'next/image';
import { redirect } from 'next/navigation';

export default async function Home() {
  const cookieStore = await cookies();
  const isLoggedIn = !!cookieStore.get('token');

  if (isLoggedIn) {
    redirect('/dashboard');
  }
  return (
    <Box className="h-screen grid place-items-center">
      <Container size="1">
        <Box className="flex flex-col items-center gap-8">
          <Image
            src="/logo.png"
            alt="Hirewise.ai Logo"
            width={500}
            height={500}
            priority
            className="items-center"
          />

          <Heading size="9" align="center" className="items-center" my="4" as="h1">
            Coming Soon
          </Heading>

          <Heading size="6" align="center" my="2" as="h2">
            Aeonik Sans Semibold H2
          </Heading>

          <Heading size="4" align="center" my="2" as="h3">
            Aeonik Sans Semibold H3
          </Heading>

          <Text size="5" align="center" color="gray" my="4" as="div">
            We&apos;re working on something exciting. Stay tuned!
          </Text>

          <Text size="3" align="center" my="2" as="p">
            This text should be displayed in Aeonik Fono regular weight. It&apos;s perfect for body
            text and provides excellent readability.
          </Text>

          <Text size="2" align="center" color="gray" my="2" as="p">
            Smaller text also uses Aeonik Fono for consistency across the design system.
          </Text>
        </Box>
      </Container>
    </Box>
  );
}
