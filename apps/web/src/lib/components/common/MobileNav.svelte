<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/stores';
	import { tick } from 'svelte';
	import { X } from '@lucide/svelte';
	import UserMenu from './UserMenu.svelte';
	import * as m from '$lib/paraglide/messages.js';

	interface Props {
		open: boolean;
		navItems: Array<{ href: string; label: string }>;
		isAuthenticated: boolean;
		onClose: () => void;
	}

	let { open = $bindable(false), navItems, isAuthenticated, onClose }: Props = $props();

	let drawer: HTMLDivElement;
	const currentPath = $derived($page.url.pathname);

	// Check if link is active
	function isActive(href: string): boolean {
		return (
			currentPath === href ||
			(href !== resolve('/(public)', {}) && currentPath.startsWith(href + '/'))
		);
	}

	// Handle link click
	function handleLinkClick() {
		onClose();
	}

	// Close on Escape key
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') onClose();
		if (event.key === 'Tab') {
			const targets = drawer.querySelectorAll<HTMLElement>(
				'a[href],button:not([disabled]),[tabindex="0"]'
			);
			const first = targets[0],
				last = targets[targets.length - 1];
			if (event.shiftKey && document.activeElement === first) {
				event.preventDefault();
				last?.focus();
			} else if (!event.shiftKey && document.activeElement === last) {
				event.preventDefault();
				first?.focus();
			}
		}
	}

	// Handle backdrop click
	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			onClose();
		}
	}

	// Focus trap management
	$effect(() => {
		if (open) {
			const previous =
				document.activeElement instanceof HTMLElement ? document.activeElement : null;
			void tick().then(() => {
				if (open) drawer.querySelector('button')?.focus();
			});
			const desktop = matchMedia('(min-width: 1280px)');
			const closeOnDesktop = () => {
				if (desktop.matches) onClose();
			};
			desktop.addEventListener('change', closeOnDesktop);
			// Keyboard focus remains inside the open navigation drawer.
			document.addEventListener('keydown', handleKeydown);
			// Prevent body scroll
			document.body.style.overflow = 'hidden';

			return () => {
				document.removeEventListener('keydown', handleKeydown);
				document.body.style.overflow = '';
				desktop.removeEventListener('change', closeOnDesktop);
				previous?.focus();
			};
		}
		return undefined;
	});
</script>

<!-- Backdrop -->
{#if open}
	<div
		class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
		onclick={handleBackdropClick}
		role="presentation"
	></div>
{/if}

<!-- Mobile Menu Drawer -->
<div
	bind:this={drawer}
	inert={!open}
	aria-hidden={!open}
	class="fixed right-0 top-0 z-50 h-full w-full max-w-sm transform border-l bg-background shadow-lg transition-transform duration-300 ease-in-out xl:hidden {open
		? 'translate-x-0'
		: 'translate-x-full'}"
	role="dialog"
	aria-modal="true"
	aria-label={m['nav.mobileNavigation']()}
>
	<div class="flex h-full flex-col">
		<!-- Header -->
		<div class="flex items-center justify-between border-b p-4">
			<span role="heading" aria-level="2" class="text-lg font-semibold">{m['nav.menu']()}</span>
			<button
				type="button"
				class="rounded-md p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:ring-2 focus:ring-ring"
				onclick={onClose}
				aria-label={m['nav.closeMenu']()}
			>
				<X class="h-6 w-6" aria-hidden="true" />
			</button>
		</div>

		<!-- Navigation Links -->
		<nav class="flex-1 overflow-y-auto p-4" aria-label={m['nav.mobileNavigation']()}>
			<ul class="space-y-2">
				{#each navItems as item (item.href)}
					<li>
						<!-- eslint-disable svelte/no-navigation-without-resolve -- href is a ResolvedPathname produced by resolve() in the nav item list above -->
						<a
							href={item.href}
							class="block rounded-md px-4 py-3 text-base transition-colors {isActive(item.href)
								? 'bg-accent font-bold text-accent-foreground'
								: 'font-semibold text-muted-foreground hover:bg-accent hover:text-accent-foreground'}"
							onclick={handleLinkClick}
							aria-current={isActive(item.href) ? 'page' : undefined}
						>
							{item.label}
						</a>
						<!-- eslint-enable svelte/no-navigation-without-resolve -->
					</li>
				{/each}
			</ul>

			<div class="mt-4 border-t pt-4">
				<a
					href={resolve('/(auth)/dashboard', {})}
					onclick={handleLinkClick}
					class="block rounded-md px-4 py-3 text-base font-medium">{m['creative.myCaudal']()}</a
				>
				<a
					href={resolve('/(auth)/producer', {})}
					onclick={handleLinkClick}
					class="block rounded-md px-4 py-3 text-sm text-muted-foreground"
					>{m['workspace.producerSpace']()}</a
				>
				{#if $page.data.workspace?.platform_admin}<a
						href={resolve('/(auth)/administration', {})}
						onclick={handleLinkClick}
						class="block rounded-md px-4 py-3 text-sm text-muted-foreground"
						>{m['workspace.administration']()}</a
					>{/if}
			</div>
			<!-- Auth Actions -->
			{#if !isAuthenticated}
				<div class="mt-6 space-y-2 border-t pt-6">
					<a
						href={resolve('/(public)/login', {})}
						class="block rounded-md px-4 py-3 text-center text-base font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
						onclick={handleLinkClick}
					>
						{m['auth.login']()}
					</a>
					<a
						href={resolve('/(public)/register', {})}
						class="block rounded-md bg-primary px-4 py-3 text-center text-base font-medium text-primary-foreground transition-colors hover:bg-primary/90"
						onclick={handleLinkClick}
					>
						{m['auth.signUp']()}
					</a>
				</div>
			{:else}
				<!-- User Menu in Mobile -->
				<div class="mt-6 border-t pt-6">
					<UserMenu mobile={true} onItemClick={handleLinkClick} />
				</div>
			{/if}
		</nav>
	</div>
</div>
