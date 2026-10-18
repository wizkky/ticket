<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, Asterisk } from '@lucide/svelte';
	import { reveal } from './reveal';
	import * as m from '$lib/paraglide/messages.js';
	const producerHref = resolve('/(auth)/producer', {});
</script>

<section id="productores" class="producer-section" aria-labelledby="producer-title">
	<div class="wrap producer-inner" use:reveal>
		<p class="eyebrow">{m['caudal.producerLabel']()}</p>
		<div class="producer-content">
			<div>
				<h2 id="producer-title">
					{m['caudal.producerTitle']()}<br /><em>{m['caudal.producerSecond']()}</em>
				</h2>
				<p>{m['caudal.producerCopy']()}</p>
				<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- producerHref is resolved above for both auth states -->
				<a class="pill" href={producerHref}
					>{m['caudal.producerAction']()}<ArrowUpRight size={20} strokeWidth={1.5} /></a
				>
			</div>
			<span class="producer-asterisk" aria-hidden="true"
				><Asterisk size="1em" strokeWidth={0.6} /></span
			>
		</div>
	</div>
</section>

<style>
	.wrap {
		width: min(100%, 1700px);
		margin-inline: auto;
		padding-inline: var(--gutter);
	}
	.eyebrow {
		font-size: 10px;
		letter-spacing: 0.17em;
		text-transform: uppercase;
		line-height: 1.6;
		font-weight: 500;
	}
	h2 {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(35px, 4.2vw, 66px);
		font-weight: 400;
		line-height: 1.14;
		letter-spacing: -0.055em;
		margin-top: 22px;
	}
	.pill {
		display: inline-flex;
		align-items: center;
		justify-content: space-between;
		gap: 30px;
		border-radius: 100px;
		padding: 17px 24px;
		background: hsl(var(--primary));
		color: hsl(var(--primary-foreground));
		font-size: 12px;
		font-weight: 500;
		transition: transform 0.25s;
	}
	.pill:hover {
		transform: translateY(-3px);
	}
	.producer-section {
		border-block: 1px solid hsl(var(--border));
		background: hsl(var(--card));
		scroll-margin-top: 90px;
	}
	.producer-inner {
		padding-block: 80px 95px;
	}
	.producer-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 40px;
	}
	.producer-content h2 {
		max-width: 850px;
	}
	.producer-content em {
		font-family: Georgia, serif;
		font-weight: 400;
	}
	.producer-content p {
		color: hsl(var(--muted-foreground));
		max-width: 390px;
		margin-block: 28px;
		line-height: 1.8;
		font-size: 14px;
	}
	.producer-asterisk {
		font-size: clamp(120px, 20vw, 300px);
		line-height: 1;
		font-weight: 300;
	}

	@media (max-width: 767px) {
		.producer-inner {
			padding-block: 60px;
		}
		.producer-content {
			display: block;
		}
		.producer-asterisk {
			display: none;
		}
		h2 {
			font-size: 36px;
		}
		.pill {
			padding: 16px 20px;
			gap: 20px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.pill {
			transition: none;
		}
	}
</style>
