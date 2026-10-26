<script lang="ts">
	import { SeoHead } from '$lib/seo';
	import { onMount } from 'svelte';
	import { asset, resolve } from '$app/paths';
	import { ArrowUpRight, ArrowDown, ArrowRight, Search, CalendarDays, Radio } from '@lucide/svelte';
	import FlowField from '$lib/components/caudal/FlowField.svelte';
	import MotionToggle from '$lib/components/caudal/MotionToggle.svelte';
	import OfferLabel from '$lib/components/caudal/OfferLabel.svelte';
	import CategoryLinks from '$lib/components/caudal/CategoryLinks.svelte';
	import CommunityPreview from '$lib/components/caudal/CommunityPreview.svelte';
	import Services from '$lib/components/caudal/Services.svelte';
	import ProducerSection from '$lib/components/caudal/ProducerSection.svelte';
	import { reveal } from '$lib/components/caudal/reveal';
	import { formatEventDate } from '$lib/utils/date';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();
	let paused = $state(false);
	onMount(() => {
		const sync = () => {
			paused = document.documentElement.dataset.caudalMotion === 'paused';
		};
		sync();
		window.addEventListener('caudal-motion-change', sync);
		return () => window.removeEventListener('caudal-motion-change', sync);
	});
</script>

<SeoHead config={data.seo} />
<svelte:head><meta name="robots" content="noindex,nofollow" /></svelte:head>

<div class="creative-home">
	<section class="hero" aria-labelledby="creative-title">
		<div class="hero-flow" aria-hidden="true"><FlowField {paused} /></div>
		<div class="hero-inner">
			<div class="hero-meta">
				<p class="creative-eyebrow"><span class="dot"></span>{m['creative.kicker']()}</p>
				<!-- i18n-ignore: geographic names --><span>Valdivia / Los Ríos, Chile</span>
			</div>
			<div class="hero-body">
				<div class="hero-copy">
					<h1 id="creative-title">{m['creative.heroOne']()} <em>{m['creative.heroTwo']()}</em></h1>
					<p>{m['creative.heroCopy']()}</p>
					<a class="creative-link" href="#descubrir"
						>{m['caudal.scroll']()}<ArrowDown size={17} aria-hidden="true" /></a
					>
				</div>
				<div class="confluence" aria-hidden="true">
					<div class="confluence-ring"></div>
					<div class="confluence-ring inner"></div>
					<div class="original-symbol">
						<img src={asset('/brand/caudal/symbol.png')} alt="" width="2048" height="2048" />
					</div>
					<span class="coordinates">39°49′ S / 73°14′ O</span>
				</div>
			</div>
			<div class="discovery-bar" id="descubrir">
				<form action={resolve('/(public)/events', {})} method="GET" role="search">
					<Search size={21} strokeWidth={1.4} aria-hidden="true" /><label
						class="sr-only"
						for="activity-search">{m['creative.searchLabel']()}</label
					>
					<input
						id="activity-search"
						name="search"
						type="search"
						placeholder={m['creative.searchPlaceholder']()}
					/>
					<button type="submit"
						>{m['creative.searchAction']()}<ArrowRight size={19} aria-hidden="true" /></button
					>
				</form>
				<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- the route is resolved before appending calendar query parameters -->
				<a class="calendar-link" href={`${resolve('/(public)/events', {})}?viewMode=calendar`}
					><CalendarDays size={18} strokeWidth={1.3} aria-hidden="true" />{m[
						'creative.openCalendar'
					]()}<ArrowUpRight size={16} aria-hidden="true" /></a
				>
			</div>
			<div class="hero-bottom"><span>{m['caudal.origin']()}</span><MotionToggle /></div>
		</div>
	</section>

	<section class="creative-section interests" aria-labelledby="interests-title">
		<div class="creative-heading" use:reveal>
			<div>
				<p class="creative-eyebrow">01 / {m['creative.explore']()}</p>
				<h2 id="interests-title">{m['creative.categoriesTitle']()}</h2>
			</div>
			<p>{m['creative.categoriesCopy']()}</p>
		</div>
		<CategoryLinks />
	</section>

	<section class="creative-section activities" aria-labelledby="activities-title">
		<div class="creative-heading" use:reveal>
			<div>
				<p class="creative-eyebrow">02 / {m['creative.nextLabel']()}</p>
				<h2 id="activities-title">{m['creative.nextTitle']()}</h2>
			</div>
			<a class="creative-link" href={resolve('/(public)/events', {})}
				>{m['creative.allActivities']()}<ArrowUpRight size={19} aria-hidden="true" /></a
			>
		</div>
		<div class="activity-grid" class:two-activities={data.events.length === 2}>
			{#each data.events as event, i (event.id)}
				<a
					class="activity-card"
					href={resolve('/(public)/events/[org_slug]/[event_slug]', {
						org_slug: event.organization.slug,
						event_slug: event.slug
					})}
					use:reveal
				>
					<div class="activity-art" class:alternate={i % 2 === 1}>
						{#if event.cover_art_thumbnail_url || event.cover_art}<img
								src={event.cover_art_thumbnail_url || event.cover_art || ''}
								alt=""
								loading="lazy"
								width="720"
								height="480"
							/>{:else}<div class="poster-lines" aria-hidden="true"></div>
							<span class="poster-name" aria-hidden="true">{event.organization.name}</span>{/if}
						<span class="activity-index" aria-hidden="true">0{i + 1} / ↗</span>
					</div>
					<div class="activity-info">
						<time datetime={event.start}>{formatEventDate(event.start, event.timezone)}</time>
						<h3>{event.name}</h3>
						<p>{event.organization.name}</p>
						<p>{event.venue?.city?.name ?? event.city?.name ?? ''}</p>
						<OfferLabel offer={data.offers[event.id]} /><span class="creative-link"
							>{m['caudal.viewEvent']()}<ArrowUpRight size={17} aria-hidden="true" /></span
						>
					</div>
				</a>
			{:else}
				<div class="creative-empty empty-activities" role="status">
					<Radio size={30} strokeWidth={1} aria-hidden="true" />
					<p>
						{data.eventsUnavailable ? m['caudal.agendaUnavailable']() : m['caudal.emptyAgenda']()}
					</p>
					<a class="creative-link" href={resolve('/(public)/events', {})}
						>{m['creative.allActivities']()}<ArrowUpRight size={18} aria-hidden="true" /></a
					>
				</div>
			{/each}
		</div>
		<p class="demo-note">{m['workspace.paymentScope']()}</p>
	</section>

	<div class="current-band" aria-hidden="true">
		<span>{m['caudal.marquee']()}</span><span>{m['creative.categoriesCopy']()}</span>
	</div>
	<CommunityPreview organizations={data.organizations} unavailable={data.communityUnavailable} />
	<Services />
	<div class="ecosystem-access">
		<a class="creative-link" href={resolve('/(public)/ecosistema', {})}
			>{m['caudal.familyTitle']()}<ArrowUpRight size={19} aria-hidden="true" /></a
		>
	</div>
	<ProducerSection />
</div>

<style>
	.creative-home {
		overflow: clip;
	}
	.hero {
		position: relative;
		border-bottom: 1px solid hsl(var(--border));
	}
	.hero-inner {
		width: min(100%, 1600px);
		margin: auto;
		padding: 32px clamp(22px, 4.7vw, 88px) 18px;
		position: relative;
	}
	.hero-flow {
		position: absolute;
		inset: 0 0 0 32%;
		opacity: 0.75;
		pointer-events: none;
	}
	.hero-meta,
	.hero-bottom {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 20px;
		font-size: 10px;
		color: hsl(var(--muted-foreground));
	}
	.hero-meta .creative-eyebrow {
		display: flex;
		align-items: center;
		gap: 12px;
		color: hsl(var(--foreground));
	}
	.dot {
		width: 6px;
		height: 6px;
		background: currentColor;
		border-radius: 50%;
	}
	.hero-body {
		display: grid;
		grid-template-columns: 1.7fr 1fr;
		align-items: center;
		gap: 35px;
		min-height: 480px;
		padding-block: 55px 45px;
	}
	h1 {
		font-size: clamp(52px, 6.3vw, 92px);
		letter-spacing: -0.065em;
		line-height: 1.04;
		font-weight: 400;
		max-width: 900px;
	}
	h1 em {
		display: block;
		font-family: Georgia, serif;
		font-weight: 400;
		letter-spacing: -0.06em;
	}
	.hero-copy > p {
		max-width: 450px;
		margin-top: 30px;
		color: hsl(var(--muted-foreground));
		font-size: 14px;
		line-height: 1.9;
	}
	.hero-copy > a {
		margin-top: 20px;
		font-size: 11px;
	}
	.confluence {
		position: relative;
		aspect-ratio: 1;
		width: 100%;
		max-width: 390px;
		justify-self: end;
	}
	.confluence-ring {
		position: absolute;
		inset: 0;
		border: 1px solid hsl(var(--border));
		border-radius: 50%;
		transform: rotate(-18deg) scaleX(0.85);
	}
	.confluence-ring.inner {
		inset: -8%;
		transform: rotate(32deg) scaleX(0.85);
		border-style: dashed;
		opacity: 0.7;
	}
	.original-symbol {
		width: 100%;
		height: 100%;
		position: relative;
		overflow: hidden;
		animation: drift 10s ease-in-out infinite;
		mix-blend-mode: multiply;
	}
	.original-symbol img {
		position: absolute;
		width: 190%;
		max-width: none;
		height: 190%;
		left: -45%;
		top: -45%;
		filter: invert(1);
		mix-blend-mode: multiply;
		object-fit: contain;
	}
	:global(.dark) .original-symbol {
		mix-blend-mode: screen;
	}
	:global(.dark) .original-symbol img {
		filter: none;
		mix-blend-mode: screen;
	}
	.coordinates {
		position: absolute;
		bottom: 0;
		right: 0;
		font-size: 9px;
		letter-spacing: 0.1em;
		background: hsl(var(--background));
		padding: 8px;
	}
	.discovery-bar {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 28px;
		align-items: center;
		scroll-margin-top: 110px;
	}
	form {
		display: flex;
		align-items: center;
		gap: 18px;
		padding: 12px 14px 12px 24px;
		border: 1px solid hsl(var(--border));
		border-radius: 50px;
		background: hsl(var(--background));
	}
	input {
		width: 100%;
		min-width: 0;
		background: transparent;
		border: 0;
		outline: none;
		font-size: 15px;
	}
	form:focus-within {
		outline: 2px solid hsl(var(--ring));
		outline-offset: 4px;
	}
	form > :global(svg) {
		flex-shrink: 0;
	}
	form button {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 24px;
		padding: 13px 20px;
		background: hsl(var(--foreground));
		color: hsl(var(--background));
		border-radius: 30px;
		font-size: 12px;
	}
	.calendar-link {
		display: inline-flex;
		align-items: center;
		gap: 12px;
		min-height: 44px;
		font-size: 12px;
	}
	.hero-bottom {
		margin-top: 25px;
	}
	.interests {
		padding-bottom: 35px;
	}
	.activity-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 26px;
	}
	.activity-grid.two-activities {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
	.activity-card {
		min-width: 0;
	}
	.activity-art {
		position: relative;
		aspect-ratio: 1.45;
		background: hsl(var(--secondary));
		overflow: hidden;
	}
	.activity-art > img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.6s;
	}
	.activity-card:hover .activity-art > img {
		transform: scale(1.04);
	}
	.poster-lines {
		position: absolute;
		inset: -60%;
		border-radius: 50%;
		background: repeating-radial-gradient(
			ellipse at 65% 50%,
			transparent 0 12px,
			hsl(var(--foreground) / 0.15) 13px 14px,
			transparent 15px 27px
		);
		transform: rotate(-35deg);
	}
	.alternate .poster-lines {
		transform: rotate(70deg);
	}
	.poster-name {
		position: absolute;
		left: 25px;
		right: 25px;
		top: 38%;
		font-family: 'Manrope', sans-serif;
		font-size: clamp(24px, 3vw, 42px);
		line-height: 1.12;
		letter-spacing: -0.05em;
		overflow-wrap: anywhere;
	}
	.activity-index {
		position: absolute;
		bottom: 16px;
		right: 18px;
		font-size: 10px;
	}
	.activity-info {
		border-bottom: 1px solid hsl(var(--border));
		padding-block: 22px 15px;
	}
	time {
		font-size: 10px;
		text-transform: uppercase;
		letter-spacing: 0.08em;
	}
	h3 {
		font-size: clamp(24px, 2.3vw, 34px);
		font-weight: 400;
		letter-spacing: -0.045em;
		line-height: 1.2;
		margin-block: 12px;
		overflow-wrap: anywhere;
	}
	.activity-info > p {
		font-size: 12px;
		color: hsl(var(--muted-foreground));
		margin-bottom: 5px;
	}
	.activity-info > .creative-link {
		width: 100%;
		margin-top: 15px;
		font-size: 11px;
	}
	.empty-activities {
		grid-column: 1 / -1;
		display: grid;
		justify-items: start;
		gap: 14px;
	}
	.demo-note {
		font-size: 10px;
		line-height: 1.8;
		color: hsl(var(--muted-foreground));
		margin-top: 22px;
		max-width: 750px;
	}
	.current-band {
		display: flex;
		justify-content: center;
		gap: 60px;
		border-block: 1px solid hsl(var(--border));
		padding: 25px;
		font-size: clamp(18px, 2.1vw, 30px);
		font-family: Georgia, serif;
		font-style: italic;
		color: hsl(var(--muted-foreground));
	}
	.current-band span {
		flex-shrink: 0;
	}
	.ecosystem-access {
		width: min(100%, 1600px);
		margin: 0 auto 55px;
		padding-inline: clamp(22px, 4.7vw, 88px);
	}
	:global(html[data-caudal-motion='paused']) .original-symbol {
		animation-play-state: paused;
	}
	@keyframes drift {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-10px);
		}
	}
	@media (max-width: 1023px) {
		.hero-body {
			grid-template-columns: 1.6fr 0.8fr;
			gap: 20px;
		}
		.discovery-bar {
			gap: 16px;
		}
		.activity-grid {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}
	@media (max-width: 767px) {
		.hero-meta {
			align-items: flex-start;
			flex-direction: column;
			gap: 10px;
		}
		.hero-body {
			display: block;
			min-height: 0;
			padding-block: 42px 30px;
		}
		h1 {
			font-size: clamp(46px, 9.8vw, 72px);
			max-width: 600px;
		}
		.hero-copy > p {
			max-width: 370px;
		}
		.confluence {
			display: none;
		}
		.hero-flow {
			inset: 0 0 0 20%;
			opacity: 0.45;
		}
		.discovery-bar {
			grid-template-columns: 1fr;
			gap: 12px;
		}
		form {
			gap: 12px;
			padding-left: 18px;
		}
		form button {
			font-size: 0;
			gap: 0;
			padding: 13px;
		}
		.calendar-link {
			justify-self: end;
		}
		.hero-bottom {
			margin-top: 12px;
			gap: 8px;
		}
		.hero-bottom > span {
			max-width: 150px;
			line-height: 1.7;
		}
		.activity-grid,
		.activity-grid.two-activities {
			grid-template-columns: 1fr;
			gap: 35px;
		}
		.current-band {
			justify-content: flex-start;
			overflow: hidden;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.original-symbol {
			animation: none;
		}
		.activity-art > img {
			transition: none;
		}
	}
</style>
