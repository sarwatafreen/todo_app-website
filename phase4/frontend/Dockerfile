FROM node:20-alpine AS builder

WORKDIR /app

# Install ALL dependencies (including devDependencies)
COPY package.json package-lock.json ./
RUN npm ci --include=dev

# Copy configuration files needed for build
COPY postcss.config.js ./
COPY tailwind.config.js ./

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build


FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app ./

EXPOSE 3000
CMD ["npm", "start"]