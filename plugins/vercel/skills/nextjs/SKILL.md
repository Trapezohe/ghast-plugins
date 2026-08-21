---
name: nextjs
description: Next.js App Router expert guidance. Use when building, debugging, or architecting Next.js applications — routing, Server Components, Server Actions, Cache Components, layouts, middleware/proxy, data fetching, rendering strategies, and deployment on Vercel.
metadata:
  priority: '5'
  docs: '["https://nextjs.org/docs","https://nextjs.org/docs/app"]'
  sitemap: https://nextjs.org/sitemap.xml
  pathPatterns: '["next.config.*","next-env.d.ts","app/**","pages/**","src/app/**","src/pages/**","tailwind.config.*","postcss.config.*","tsconfig.json","tsconfig.*.json","apps/*/app/**","apps/*/pages/**","apps/*/src/app/**","apps/*/src/pages/**","apps/*/next.config.*"]'
  bashPatterns: '["\\bnext\\s+(dev|build|start|lint)\\b","\\bnext\\s+experimental-analyze\\b","\\bnpx\\s+create-next-app\\b","\\bbunx\\s+create-next-app\\b","\\bnpm\\s+run\\s+(dev|build|start)\\b","\\bpnpm\\s+(dev|build)\\b","\\bbun\\s+run\\s+(dev|build)\\b"]'
  promptSignals: '{"allOf":[["middleware","next"],["layout","route"]],"anyOf":["pages router","getserversideprops","use server"],"minScore":6,"noneOf":[],"phrases":["next.js","nextjs","app router","server component","server action"]}'
  validate: '[{"message":"getServerSideProps is removed in App Router — use server components or route handlers","pattern":"export.*getServerSideProps","severity":"error","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from Pages Router getServerSideProps to App Router server components with async data fetching."},{"message":"getServerSideProps is a Pages Router pattern — migrate to App Router server components","pattern":"getServerSideProps","severity":"warn"},{"message":"getStaticProps is removed in App Router — use generateStaticParams + server components instead","pattern":"export.*getStaticProps","severity":"error","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from Pages Router getStaticProps to App Router generateStaticParams with server components."},{"message":"getStaticProps is a Pages Router pattern — migrate to App Router generateStaticParams + server components","pattern":"getStaticProps","severity":"warn"},{"message":"next/router is Pages Router only — use
    next/navigation for App Router","pattern":"from\\s+[''\"]next/router[''\"]","severity":"error","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from next/router to next/navigation with useRouter, usePathname, useSearchParams hooks."},{"message":"React hooks require \"use client\" directive — add it at the top of client components","pattern":"(useState|useEffect)","severity":"warn","skipIfFileContains":"^[''\"]use client[''\"]"},{"message":"next/head is Pages Router — use export const metadata or generateMetadata() in App Router. Run Skill(nextjs) for metadata API guidance.","pattern":"from\\s+[''\"]next/head[''\"]","severity":"error","skipIfFileContains":"export\\s+(const\\s+)?metadata|generateMetadata","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from next/head to the App Router metadata API (export const metadata / generateMetadata())."},{"message":"middleware() is renamed to proxy() in Next.js 16 — rename the function and the file to proxy.ts. Run Skill(routing-middleware)
    for proxy.ts migration guidance.","pattern":"export\\s+(default\\s+)?function\\s+middleware","severity":"recommended","upgradeToSkill":"routing-middleware","upgradeWhy":"Guides migration from middleware.ts to proxy.ts with correct file placement, runtime config, and request interception patterns."},{"message":"Single-arg revalidateTag(tag) is deprecated in Next.js 16 — pass a cacheLife profile: revalidateTag(tag, \"max\")","pattern":"revalidateTag\\(\\s*[''\"][^''\"]+[''\"]\\s*\\)","severity":"recommended","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from single-arg revalidateTag to the Next.js 16 two-arg API with cacheLife profiles."},{"message":"Singular cacheHandler is deprecated in Next.js 16 — use cacheHandlers (plural) with per-type handlers","pattern":"\\bcacheHandler\\s*:","severity":"recommended","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from singular cacheHandler to Next.js 16 cacheHandlers (plural) with per-type handler config."},{"message":"useRef()
    requires an initial value in React 19 — use useRef(null) or useRef(0)","pattern":"useRef\\(\\s*\\)","severity":"error"},{"message":"next export was removed — use output: \"export\" in next.config.js for static export","pattern":"next\\s+export","severity":"error","upgradeToSkill":"nextjs","upgradeWhy":"Guides migration from next export CLI command to output: \"export\" in next.config for static site generation."},{"message":"cookies() is async in Next.js 16 — add await: const cookieStore = await cookies()","pattern":"(?<!await )\\bcookies\\(\\s*\\)","severity":"error","skipIfFileContains":"^[''\"]use client[''\"]"},{"message":"headers() is async in Next.js 16 — add await: const headersList = await headers()","pattern":"(?<!await )\\bheaders\\(\\s*\\)","severity":"error","skipIfFileContains":"^[''\"]use client[''\"]"},{"message":"params is async in Next.js 16 — add await: const { slug } = await params","pattern":"=\\s*(?!await\\b)params\\b","severity":"recommended","skipIfFileContains":"^[''\"]use
    client[''\"]"},{"message":"searchParams is async in Next.js 16 — add await: const { query } = await searchParams","pattern":"=\\s*(?!await\\b)searchParams\\b","severity":"recommended","skipIfFileContains":"^[''\"]use client[''\"]"},{"message":"Legacy auth pattern detected. Modern Vercel apps should use Clerk, Descope, or Auth0 for managed authentication.","pattern":"from\\s+[''\"\"](next-auth|@auth/core)[''\"\"]|NextAuth\\(|getServerSession\\(","severity":"recommended","skipIfFileContains":"@clerk/|@descope/|@auth0/","upgradeToSkill":"auth","upgradeWhy":"Migrate from next-auth/manual JWT to a managed auth provider (Clerk, Descope, Auth0) for better Vercel integration."},{"message":"Pages Router API handler detected. Use App Router route handlers with named HTTP exports instead.","pattern":"NextApiRequest|NextApiResponse|export\\s+default\\s+function\\s+handler","severity":"recommended","skipIfFileContains":"export\\s+(async\\s+)?function\\s+(GET|POST|PUT|PATCH|DELETE)","upgradeToSkill":"vercel-functions","upgradeWhy":"Migrate
    from Pages Router API routes to App Router route handlers with Web Request/Response API."},{"message":"In-process cache detected. Serverless deployments lose process memory between invocations.","pattern":"from\\s+[''\"\"](lru-cache|node-cache|memory-cache)[''\"\"]|new\\s+(LRUCache|NodeCache)\\(","severity":"recommended","upgradeToSkill":"runtime-cache","upgradeWhy":"Replace process-memory caches with Vercel Runtime Cache for shared, region-aware caching."},{"message":"Express/Fastify/Koa/Hapi server framework detected in a Next.js project. Use Next.js route handlers or proxy.ts for request handling instead.","pattern":"from\\s+[''\"\"](express|fastify|koa|hapi)[''\"\"]|require\\s*\\(\\s*[''\"\"](express|fastify|koa|hapi)[''\"\"]","severity":"recommended","skipIfFileContains":"proxy\\.ts|from\\s+[''\"\"](next/server)[''\"\"]|@vercel/functions","upgradeToSkill":"routing-middleware","upgradeWhy":"Replace custom server frameworks with Next.js proxy.ts for request interception and route
    handlers for API endpoints."},{"message":"Heavy ORM detected. Consider using lightweight serverless-native alternatives like Drizzle, Prisma, or direct Neon for better cold start performance.","pattern":"from\\s+[''\"\"](typeorm|sequelize|mikro-orm|objection|bookshelf|knex)[''\"\"]|require\\s*\\(\\s*[''\"\"](typeorm|sequelize|mikro-orm|objection|bookshelf|knex)[''\"\"]","severity":"recommended","skipIfFileContains":"from\\s+[''\"\"](drizzle-orm|@neondatabase|@prisma/client|prisma)[''\"\"]","upgradeToSkill":"vercel-storage","upgradeWhy":"Migrate from heavy ORMs to serverless-native database clients (Drizzle + Neon, Prisma, or @neondatabase/serverless) for faster cold starts."},{"message":"External font loader detected. Use next/font for zero-CLS, self-hosted font loading with automatic optimization.","pattern":"fonts\\.googleapis\\.com|from\\s+[''\"\"](fontsource|@fontsource)[''\"\"]|<link[^>]*fonts\\.googleapis","severity":"recommended","skipIfFileContains":"next/font","upgradeToSkill":"nextjs","upgradeWhy":"Guides
    migration from external font loaders to next/font with Geist Sans/Mono for zero-CLS font optimization."}]'
  chainTo: '[{"message":"middleware() is renamed to proxy() in Next.js 16 — loading Routing Middleware guidance for proxy.ts migration.","pattern":"export\\s+(default\\s+)?function\\s+middleware","targetSkill":"routing-middleware"},{"message":"Sunset storage package detected — loading Vercel Storage guidance for Neon/Upstash migration.","pattern":"from\\s+[''\"]@vercel/(postgres|kv)[''\"]","targetSkill":"vercel-storage"},{"message":"Direct AI provider SDK import — loading AI Gateway guidance for unified model routing with failover and cost tracking.","pattern":"from\\s+[''\"]@ai-sdk/(anthropic|openai)[''\"]","targetSkill":"ai-gateway"},{"message":"Legacy auth pattern detected — loading managed authentication guidance (Clerk, Descope, Auth0).","pattern":"from\\s+[''\"\"](next-auth|@auth/core)[''\"\"]|NextAuth\\(|getServerSession\\(","targetSkill":"auth"},{"message":"Pages Router API handler detected — loading Vercel Functions guidance for App Router migration.","pattern":"NextApiRequest|NextApiResponse|export\\s+default\\s+function\\s+handler","targetSkill":"vercel-functions"},{"message":"In-process
    cache detected — loading Runtime Cache guidance for serverless-compatible caching.","pattern":"from\\s+[''\"\"](lru-cache|node-cache|memory-cache)[''\"\"]|new\\s+(LRUCache|NodeCache)\\(","targetSkill":"runtime-cache"},{"message":"Raw AI provider fetch URL detected — loading AI Gateway guidance for unified routing, failover, and OIDC auth.","pattern":"fetch\\s*\\(\\s*[''\"\"](https?://)?(api\\.openai\\.com|api\\.anthropic\\.com|api\\.cohere\\.ai)","skipIfFileContains":"@ai-sdk/|from\\s+[''\"\"](ai)[''\"\"]|ai-gateway|gateway\\(","targetSkill":"ai-gateway"},{"message":"Manual JWT token handling detected — loading Auth guidance for managed authentication (Clerk, Descope, Auth0).","pattern":"jwt\\.(sign|verify|decode)\\(|from\\s+[''\"\"](jsonwebtoken)[''\"\"]|new\\s+SignJWT\\(|jwtVerify\\(","skipIfFileContains":"clerkMiddleware|@clerk/|@auth0/|@descope/|from\\s+[''\"\"](next-auth)[''\"\"]","targetSkill":"auth"},{"message":"shadcn/ui component imports detected — loading shadcn guidance for
    component composition, theming, and registry patterns.","pattern":"from\\s+[''\"]@/components/ui/|from\\s+[''\"]@/components/ui[''\"\"]","skipIfFileContains":"shadcn|components\\.json","targetSkill":"shadcn"},{"message":"CSS-in-JS library detected — loading shadcn/ui guidance for Tailwind CSS + Radix UI component patterns (Vercel recommended).","pattern":"from\\s+[''\"\"](styled-components|@emotion/(react|styled)|@mui/material)[''\"\"]","skipIfFileContains":"@/components/ui|shadcn","targetSkill":"shadcn"},{"message":"getInitialProps is a legacy Pages Router pattern — loading Next.js guidance for App Router migration with server components and async data fetching.","pattern":"getInitialProps","skipIfFileContains":"app/.*page\\.|generateStaticParams|use cache","targetSkill":"nextjs"},{"message":"getServerSideProps is a Pages Router pattern — loading Next.js guidance for App Router migration with server components and async data fetching.","pattern":"export.*getServerSideProps|getServerSideProps\\s*\\(","skipIfFileContains":"generateStaticParams|use
    cache|app/.*page\\.","targetSkill":"nextjs"},{"message":"getStaticProps is a Pages Router pattern — loading Next.js guidance for App Router migration with generateStaticParams and server components.","pattern":"export.*getStaticProps|getStaticProps\\s*\\(","skipIfFileContains":"generateStaticParams|use cache|app/.*page\\.","targetSkill":"nextjs"},{"message":"_app.tsx is a Pages Router pattern — loading Next.js guidance for App Router layout.tsx migration.","pattern":"_app\\.(tsx?|jsx?)","skipIfFileContains":"app/layout\\.|app/.*layout\\.","targetSkill":"nextjs"},{"message":"_document.tsx is a Pages Router pattern — loading Next.js guidance for App Router layout.tsx with metadata API migration.","pattern":"_document\\.(tsx?|jsx?)","skipIfFileContains":"app/layout\\.|app/.*layout\\.","targetSkill":"nextjs"},{"message":"next/document is Pages Router only — loading Next.js guidance for App Router layout.tsx with html/body structure.","pattern":"from\\s+[''\"]next/document[''\"]","skipIfFileContains":"app/layout\\.|app/.*layout\\.","targetSkill":"nextjs"},{"message":"Pages
    Router API route (pages/api/) detected — loading Vercel Functions guidance for App Router route handlers with named HTTP exports.","pattern":"pages/api/","skipIfFileContains":"export\\s+(async\\s+)?function\\s+(GET|POST|PUT|PATCH|DELETE)","targetSkill":"vercel-functions"}]'
  retrieval: '{"aliases":["next.js","nextjs app","react framework","app router"],"entities":["App Router","Server Components","Server Actions","generateMetadata","layout","proxy","next.config"],"examples":["add a new page with dynamic routing","should this be a server or client component","set up middleware for auth redirects","configure caching for this data fetch","set up server rendering for my pages"],"intents":["set up routing and layouts in a Next.js app","choose between server and client components for a feature","configure data fetching or caching in App Router","add middleware or proxy logic to handle requests","set up server rendering for React pages","add a new page with dynamic route segments"]}'
---
# Next.js Best Practices

Apply these rules when writing or reviewing Next.js code.

## File Conventions

See [file-conventions.md](./file-conventions.md) for:
- Project structure and special files
- Route segments (dynamic, catch-all, groups)
- Parallel and intercepting routes
- Middleware rename in v16 (middleware → proxy)

## RSC Boundaries

Detect invalid React Server Component patterns.

See [rsc-boundaries.md](./rsc-boundaries.md) for:
- Async client component detection (invalid)
- Non-serializable props detection
- Server Action exceptions

## Async Patterns

Next.js 15+ async API changes.

See [async-patterns.md](./async-patterns.md) for:
- Async `params` and `searchParams`
- Async `cookies()` and `headers()`
- Migration codemod

## Runtime Selection

See [runtime-selection.md](./runtime-selection.md) for:
- Default to Node.js runtime
- When Edge runtime is appropriate

## Directives

See [directives.md](./directives.md) for:
- `'use client'`, `'use server'` (React)
- `'use cache'` (Next.js)

## Functions

See [functions.md](./functions.md) for:
- Navigation hooks: `useRouter`, `usePathname`, `useSearchParams`, `useParams`
- Server functions: `cookies`, `headers`, `draftMode`, `after`
- Generate functions: `generateStaticParams`, `generateMetadata`

## Error Handling

See [error-handling.md](./error-handling.md) for:
- `error.tsx`, `global-error.tsx`, `not-found.tsx`
- `redirect`, `permanentRedirect`, `notFound`
- `forbidden`, `unauthorized` (auth errors)
- `unstable_rethrow` for catch blocks

## Data Patterns

See [data-patterns.md](./data-patterns.md) for:
- Server Components vs Server Actions vs Route Handlers
- Avoiding data waterfalls (`Promise.all`, Suspense, preload)
- Client component data fetching

## Route Handlers

See [route-handlers.md](./route-handlers.md) for:
- `route.ts` basics
- GET handler conflicts with `page.tsx`
- Environment behavior (no React DOM)
- When to use vs Server Actions

## Metadata & OG Images

See [metadata.md](./metadata.md) for:
- Static and dynamic metadata
- `generateMetadata` function
- OG image generation with `next/og`
- File-based metadata conventions

## Image Optimization

See [image.md](./image.md) for:
- Always use `next/image` over `<img>`
- Remote images configuration
- Responsive `sizes` attribute
- Blur placeholders
- Priority loading for LCP

## Font Optimization

See [font.md](./font.md) for:
- `next/font` setup
- Google Fonts, local fonts
- Tailwind CSS integration
- Preloading subsets

## Bundling

See [bundling.md](./bundling.md) for:
- Server-incompatible packages
- CSS imports (not link tags)
- Polyfills (already included)
- ESM/CommonJS issues
- Bundle analysis

## Scripts

See [scripts.md](./scripts.md) for:
- `next/script` vs native script tags
- Inline scripts need `id`
- Loading strategies
- Google Analytics with `@next/third-parties`

## Hydration Errors

See [hydration-error.md](./hydration-error.md) for:
- Common causes (browser APIs, dates, invalid HTML)
- Debugging with error overlay
- Fixes for each cause

## Suspense Boundaries

See [suspense-boundaries.md](./suspense-boundaries.md) for:
- CSR bailout with `useSearchParams` and `usePathname`
- Which hooks require Suspense boundaries

## Parallel & Intercepting Routes

See [parallel-routes.md](./parallel-routes.md) for:
- Modal patterns with `@slot` and `(.)` interceptors
- `default.tsx` for fallbacks
- Closing modals correctly with `router.back()`

## Self-Hosting

See [self-hosting.md](./self-hosting.md) for:
- `output: 'standalone'` for Docker
- Cache handlers for multi-instance ISR
- What works vs needs extra setup

## Debug Tricks

See [debug-tricks.md](./debug-tricks.md) for:
- MCP endpoint for AI-assisted debugging
- Rebuild specific routes with `--debug-build-paths`

