// Custom ESLint base config for hirewise monorepo
// Usage: import this file in your .eslintrc.js as: import config from 'eslint-config/base'

export default [
  {
    rules: {
      'no-console': 'warn',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
