import { FlatCompat } from '@eslint/eslintrc';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

export default [
  ...compat.extends('airbnb-base'),
  {
    rules: {
      // airbnb uses 2 spaces, keeping it consistent
      'no-console': 'off',
    },
  },
];
