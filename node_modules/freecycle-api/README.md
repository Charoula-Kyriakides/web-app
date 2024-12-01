# Freecycle API

Library for fetching data from freecycle.org

## Install

Add the package:

```bash
# npm
npm install freecycle-api

# yarn
yarn add freecycle-api

# pnpm
pnpm add freecycle-api
```

## Usage

The library exports two functions `fetchTowns` and `fetchPosts`, which are both fully typed.

```javascript
import { fetchTowns, fetchPosts } from "freecycle-api";

// Fetch all the towns available on Freecycle
const groupData = await fetchTowns();
// => { groups: { name: string, .. }, .. }

// Fetch all the posts for a given town
const townData = await fetchPosts("BirminghamUK");
// => { posts: { id: string, .. }, .. }

// Example: find all the available offers
const offersInBirmingham = townData.posts.filter(
  ({ type }) => type.const === "FC_POST_OFFER"
);
```
