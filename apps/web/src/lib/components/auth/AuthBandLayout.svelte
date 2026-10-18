<script lang="ts">
	import type { Snippet } from 'svelte';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import { cn } from '$lib/utils';

	/**
	 * The auth cluster's poster-grade Celebration shell (uplift, spec §9).
	 *
	 * Every sign-in / sign-up / recovery / interstitial screen was the same
	 * vertically-centred column of white-on-paper: a hand-set kicker + h1, then
	 * a card. This gives the whole cluster the language U1 shipped on the public
	 * questionnaire route — a full-strength colour-block band carrying the type,
	 * with the content pulled up over its bottom edge so cards visibly FLOAT on
	 * colour rather than lying on the page.
	 *
	 * Why `bg-secondary` at full strength: `secondary` / `secondary-foreground`
	 * is an audit-enforced pair in BOTH modes (periwinkle in light, deep indigo
	 * in dark), so the band is a real poster panel that still respects the
	 * light/dark axis — no mode-inert surface, no hand-computed alpha. The
	 * kicker and subtitle inherit the band's own foreground via PageHeader's
	 * `onBand` affordance (its default `text-primary` kicker measures 4.12:1 on
	 * the light band, below AA — see PageHeader's `onBand` doc comment).
	 *
	 * Purely presentational: no form logic, no navigation, no copy of its own.
	 * The h1 it renders is the page's only heading, with byte-identical text to
	 * what each route passed before.
	 */
	interface Props {
		/** Already-translated strings — i18n stays at the call site. */
		title: string;
		kicker?: string;
		subtitle?: string;
		/**
		 * Decorative ornament rendered centred in the band ABOVE the title —
		 * the interstitials' status chip, or a `brand/LogoChip`. Callers are
		 * responsible for marking it `aria-hidden`; it must never carry copy
		 * that isn't already in the heading or body (same rule as PageHeader's
		 * `decoration` slot).
		 */
		chip?: Snippet;
		/** Column width for both the band copy and the floating stack. */
		width?: 'md' | 'lg' | 'xl';
		/**
		 * Marks the band's heading block as a live region (`role="status"`).
		 * For the interstitials whose success state is reached IN PLACE (a form
		 * submit with no navigation), where the h1 + body are the announcement.
		 * The chip is aria-hidden ornament either way, so nothing is lost by the
		 * region now starting at the header instead of the old wrapper div.
		 */
		status?: boolean;
		/**
		 * The floating content. Cards already carry the 2px edge + poster float.
		 * Optional because some interstitials (a successful verification, say)
		 * are the band and nothing else.
		 */
		children?: Snippet;
		class?: string;
	}
	const {
		title,
		kicker,
		subtitle,
		chip,
		width = 'md',
		status = false,
		children,
		class: className = ''
	}: Props = $props();

	const widthClass = $derived(
		width === 'md' ? 'max-w-md' : width === 'lg' ? 'max-w-lg' : 'max-w-2xl'
	);
</script>

<div class={cn('auth-shell', className)}>
	<section class="auth-intro">
		<div class="auth-heading">
			{#if chip}<div class="mb-6">{@render chip()}</div>{/if}
			<PageHeader
				volume="poster"
				{kicker}
				{title}
				{subtitle}
				role={status ? 'status' : undefined}
			/>
			<div class="auth-current" aria-hidden="true"></div>
		</div>
	</section>
	{#if children}<div class={cn('auth-content caudal-motion', widthClass)}>
			{@render children()}
		</div>{/if}
</div>

<style>
	.auth-shell {
		max-width: 1440px;
		margin: auto;
		min-height: 70svh;
		display: grid;
		gap: 50px;
		padding: 65px clamp(22px, 4.7vw, 88px);
	}
	.auth-heading {
		position: relative;
		max-width: 560px;
	}
	.auth-current {
		position: relative;
		height: 140px;
		margin-top: 40px;
		overflow: hidden;
		background: repeating-radial-gradient(
			ellipse at 80% -15%,
			transparent 0 14px,
			hsl(var(--foreground) / 0.15) 15px,
			transparent 16px
		);
		mask-image: linear-gradient(90deg, transparent, black);
	}
	.auth-content {
		width: 100%;
		justify-self: center;
		display: flex;
		flex-direction: column;
		gap: 24px;
	}
	@media (min-width: 1024px) {
		.auth-shell {
			grid-template-columns: 1.1fr 1fr;
			align-items: start;
			padding-block: 95px;
			gap: 90px;
		}
		.auth-content {
			justify-self: end;
		}
	}
	@media (max-width: 1023px) {
		.auth-current {
			display: none;
		}
		.auth-intro {
			max-width: 672px;
			width: 100%;
			margin: auto;
		}
		.auth-content {
			justify-self: start;
			margin: auto;
		}
	}
	@media (prefers-reduced-motion: no-preference) {
		.auth-content {
			animation: appear 0.4s ease-out both;
		}
		@keyframes appear {
			from {
				opacity: 0.6;
				transform: translateY(8px);
			}
			to {
				opacity: 1;
				transform: none;
			}
		}
	}
</style>
