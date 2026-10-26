<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth.svelte';
	import { Menu } from '@lucide/svelte';
	import MobileNav from './MobileNav.svelte';
	import UserMenu from './UserMenu.svelte';
	import ThemeToggle from './ThemeToggle.svelte';
	import LanguageSwitcher from './LanguageSwitcher.svelte';
	import { NotificationDropdown } from '$lib/components/notifications';
	import * as m from '$lib/paraglide/messages.js';
	import RevelWordmark from '$lib/components/brand/RevelWordmark.svelte';

	// Mobile menu state
	let mobileMenuOpen = $state(false);

	// Get auth state
	const isAuthenticated = $derived(authStore.isAuthenticated);
	const accessToken = $derived(authStore.accessToken);
	const currentPath = $derived($page.url.pathname);

	// Shared ecosystem navigation; organization tools remain in the authenticated user menu.
	const navItems = $derived([
		{ href: resolve('/(public)', {}), label: m['creative.home']() },
		{ href: resolve('/(public)/events', {}), label: m['creative.explore']() },
		{ href: resolve('/(public)/agenda', {}), label: m['creative.agenda']() },
		{ href: resolve('/(public)/comunidad', {}), label: m['creative.community']() },
		{ href: resolve('/(public)/ecosistema', {}), label: m['creative.ecosystem']() }
	]);

	// Check if link is active
	function isActive(href: string): boolean {
		return (
			currentPath === href ||
			(href !== resolve('/(public)', {}) && currentPath.startsWith(href + '/'))
		);
	}

	// Close mobile menu
	function closeMobileMenu() {
		mobileMenuOpen = false;
	}
</script>

<!-- Skip to main content link (accessibility) -->
<a
	href="#main-content"
	class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground focus:outline-none focus:ring-2 focus:ring-ring"
>
	{m['nav.skipToContent']()}
</a>

<header
	class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
>
	<div class="caudal-header-inner mx-auto flex h-[88px] items-center justify-between gap-4">
		<!-- Logo -->
		<div class="flex min-w-0 items-center gap-7">
			<a
				href={resolve('/(public)', {})}
				class="shrink-0 text-foreground transition-opacity hover:opacity-80"
			>
				<!-- Shared Caudal identity, including the supplied confluence symbol. -->
				<RevelWordmark class="text-xl" />
			</a>

			<!-- Desktop Navigation -->
			<nav
				class="hidden xl:flex xl:items-center xl:gap-5"
				aria-label={m['header.mainNavigation']()}
			>
				{#each navItems as item (item.href)}
					<!-- eslint-disable svelte/no-navigation-without-resolve -- href is a ResolvedPathname produced by resolve() in the nav item list above -->
					<a
						href={item.href}
						class="text-sm transition-colors hover:text-primary {isActive(item.href)
							? 'font-medium text-primary'
							: 'font-normal text-muted-foreground'}"
						aria-current={isActive(item.href) ? 'page' : undefined}
					>
						{item.label}
					</a>
					<!-- eslint-enable svelte/no-navigation-without-resolve -->
				{/each}
			</nav>
		</div>

		<!-- Right side actions -->
		<div class="flex items-center gap-2 sm:gap-4">
			<!-- Theme Toggle -->
			<ThemeToggle />

			{#if isAuthenticated}
				<!-- Notification Dropdown -->
				{#if accessToken}
					<NotificationDropdown authToken={accessToken} />
				{/if}

				<a
					href={resolve('/(auth)/dashboard', {})}
					class="hidden rounded-full border px-4 py-2 text-xs xl:inline-flex"
					>{m['creative.myCaudal']()}</a
				>
				<!-- User Menu (Desktop) -->
				<div class="hidden xl:block">
					<UserMenu />
				</div>
			{:else}
				<!-- Auth Buttons (Desktop) -->
				<div class="hidden items-center gap-2 xl:flex">
					<a
						href={resolve('/(public)/login', {})}
						class="rounded-md px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
					>
						{m['auth.login']()}
					</a>
					<a
						href={resolve('/(public)/register', {})}
						class="rounded-full bg-primary px-5 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
					>
						{m['auth.signUp']()}
					</a>
				</div>
			{/if}

			<!-- Mobile Menu Button -->
			<button
				type="button"
				class="inline-flex items-center justify-center rounded-md p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:ring-2 focus:ring-ring xl:hidden"
				onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
				aria-expanded={mobileMenuOpen}
				aria-label={m['nav.toggleMenu']()}
			>
				<Menu class="h-6 w-6" aria-hidden="true" />
			</button>

			<!-- Language Switcher (Rightmost) -->
			<LanguageSwitcher />
		</div>
	</div>
</header>

<!-- Mobile Navigation -->
<MobileNav bind:open={mobileMenuOpen} {navItems} {isAuthenticated} onClose={closeMobileMenu} />

<style>
	.caudal-header-inner {
		width: min(100%, 1700px);
		padding-inline: clamp(22px, 4.7vw, 88px);
	}
	nav a {
		position: relative;
	}
	nav a::after {
		content: '';
		position: absolute;
		bottom: -7px;
		left: 0;
		width: 100%;
		height: 1px;
		background: currentColor;
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 0.25s;
	}
	nav a:hover::after,
	nav a[aria-current='page']::after {
		transform: scaleX(1);
	}
	@media (max-width: 767px) {
		.caudal-header-inner :global(.caudal-wordmark) {
			width: min(130px, calc(100vw - 240px));
		}
		.caudal-header-inner {
			height: 76px;
			gap: 8px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		nav a::after {
			transition: none;
		}
	}
</style>
