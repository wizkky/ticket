<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import {
		ArrowUpRight,
		ArrowDown,
		ArrowRight,
		Search,
		Pause,
		Play,
		Ticket,
		QrCode,
		Radio
	} from '@lucide/svelte';
	import OfferLabel from '$lib/components/caudal/OfferLabel.svelte';
	import FlowField from '$lib/components/caudal/FlowField.svelte';
	import FloatingTicket from '$lib/components/caudal/FloatingTicket.svelte';
	import Family from '$lib/components/caudal/Family.svelte';
	import { reveal } from '$lib/components/caudal/reveal';
	import { formatEventDate } from '$lib/utils/date';
	import ProducerSection from '$lib/components/caudal/ProducerSection.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();
	let paused = $state(false);
	let reduced = $state(false);
	const motionStopped = $derived(paused || reduced);

	onMount(() => {
		const preference = matchMedia('(prefers-reduced-motion: reduce)');
		const sync = () => {
			reduced = preference.matches;
		};
		sync();
		preference.addEventListener('change', sync);
		try {
			paused = localStorage.getItem('caudal-motion') === 'paused';
		} catch {
			/* optional preference */
		}
		const syncPause = () => {
			paused = document.documentElement.dataset.caudalMotion === 'paused';
		};
		window.addEventListener('caudal-motion-change', syncPause);
		return () => {
			preference.removeEventListener('change', sync);
			window.removeEventListener('caudal-motion-change', syncPause);
		};
	});
	function toggleMotion() {
		paused = !paused;
		document.documentElement.dataset.caudalMotion = paused ? 'paused' : 'playing';
		if (paused) window.dispatchEvent(new Event('caudal-motion-paused'));
		try {
			localStorage.setItem('caudal-motion', paused ? 'paused' : 'playing');
			window.dispatchEvent(new Event('caudal-motion-change'));
		} catch {
			/* optional preference */
		}
	}
</script>

<svelte:head>
	<title>{m['caudal.metaTitle']()}</title>
	<meta name="description" content={m['workspace.territoryIntro']()} />
	<meta name="robots" content="noindex,nofollow" />
</svelte:head>

<div class="caudal-home" class:motion-paused={motionStopped}>
	<section class="hero" aria-labelledby="caudal-title">
		<div class="flow-field"><FlowField paused={motionStopped} /></div>
		<div class="hero-meta wrap">
			<span class="eyebrow"><i></i>{m['caudal.eyebrow']()}</span
			><!-- i18n-ignore: geographic name --><span class="location">Valdivia / Los Ríos, Chile</span>
		</div>
		<div class="hero-body wrap">
			<div class="hero-copy">
				<h1 id="caudal-title">
					<span>{m['caudal.heroOne']() + ' '}</span><span class="second-line"
						>{m['caudal.heroTwo']()}</span
					>
				</h1>
				<p>{m['workspace.territoryIntro']()}</p>
				<div class="hero-actions">
					<a class="pill" href={resolve('/(public)/events', {})}
						>{m['caudal.explore']()}<ArrowUpRight size={19} strokeWidth={1.5} /></a
					><a class="text-link" href="#productores"
						>{m['caudal.forProducers']()}<ArrowUpRight size={16} strokeWidth={1.5} /></a
					>
				</div>
			</div>
			<div class="hero-object"><FloatingTicket paused={motionStopped} /></div>
		</div>
		<div class="hero-bottom wrap">
			<a href="#agenda" class="scroll-link"
				><span><ArrowDown size={15} strokeWidth={1.2} /></span>{m['caudal.scroll']()}</a
			>
			<p>{m['caudal.origin']()}</p>
			<button
				type="button"
				onclick={toggleMotion}
				aria-pressed={paused}
				disabled={reduced}
				class="motion-toggle"
			>
				{#if motionStopped}<Play size={12} aria-hidden="true" />{:else}<Pause
						size={12}
						aria-hidden="true"
					/>{/if}
				{reduced ? m['caudal.reducedMotion']() : paused ? m['caudal.play']() : m['caudal.pause']()}
			</button>
		</div>
	</section>

	<section id="agenda" class="agenda wrap section-space" aria-labelledby="agenda-title">
		<div class="section-heading" use:reveal>
			<div>
				<p class="eyebrow">{m['caudal.agendaLabel']()}</p>
				<h2 id="agenda-title">{m['caudal.agendaTitle']()}</h2>
			</div>
			<a class="text-link" href={resolve('/(public)/events', {})}
				>{m['caudal.allEvents']()}<ArrowUpRight size={19} /></a
			>
		</div>
		<form class="event-search" action={resolve('/(public)/events', {})} method="GET" role="search">
			<Search size={19} strokeWidth={1.4} aria-hidden="true" /><label
				class="sr-only"
				for="event-search">{m['caudal.searchLabel']()}</label
			><input
				id="event-search"
				name="search"
				type="search"
				placeholder={m['caudal.searchPlaceholder']()}
			/><button type="submit" aria-label={m['caudal.searchButton']()}
				><ArrowRight size={20} strokeWidth={1.5} /></button
			>
		</form>
		<div class="event-grid" class:two-events={data.events.length === 2}>
			{#each data.events as event, i (event.id)}
				<a
					class="event-card"
					href={resolve('/(public)/events/[org_slug]/[event_slug]', {
						org_slug: event.organization.slug,
						event_slug: event.slug
					})}
					use:reveal
				>
					<div class="event-art" class:alternate={i % 2 === 1}>
						{#if event.cover_art_thumbnail_url || event.cover_art}<img
								src={event.cover_art_thumbnail_url || event.cover_art || ''}
								alt=""
								loading="lazy"
								width="720"
								height="480"
							/>{:else}<div class="poster-lines" aria-hidden="true"></div>
							<span class="poster-title" aria-hidden="true">{event.organization.name}</span>{/if}
						<span class="event-index" aria-hidden="true">0{i + 1} / ↗</span>
					</div>
					<div class="event-details">
						<p class="event-date">
							<time datetime={event.start}>{formatEventDate(event.start, event.timezone)}</time>
						</p>
						<h3>{event.name}</h3>
						<p class="event-organizer">{event.organization.name}</p>
						<p class="event-organizer">{event.venue?.city?.name ?? event.city?.name ?? ''}</p>
						<OfferLabel offer={data.offers[event.id]} />
						<span class="event-cta">{m['caudal.viewEvent']()}<ArrowUpRight size={17} /></span>
					</div>
				</a>
			{:else}
				<div class="agenda-empty">
					<Radio size={32} strokeWidth={1} aria-hidden="true" />
					<p>
						{data.eventsUnavailable ? m['caudal.agendaUnavailable']() : m['caudal.emptyAgenda']()}
					</p>
					<a class="text-link" href={resolve('/(public)/events', {})}
						>{m['caudal.explore']()}<ArrowUpRight size={18} /></a
					>
				</div>
			{/each}
		</div>
		<p class="demo-note">{m['workspace.paymentScope']()}</p>
	</section>

	<div class="marquee" aria-hidden="true">
		<div class="marquee-track">
			{#each [0, 1, 2, 3] as n (n)}<span>{m['caudal.marquee']()}</span>{/each}
		</div>
	</div>

	<section class="wrap section-space journey" aria-labelledby="journey-title">
		<div class="section-heading" use:reveal>
			<div>
				<p class="eyebrow">{m['caudal.flowLabel']()}</p>
				<h2 id="journey-title">{m['caudal.flowTitle']()}</h2>
			</div>
		</div>
		<div class="journey-grid">
			<article use:reveal>
				<div class="step-top"><span>01</span><ArrowUpRight size={28} strokeWidth={1} /></div>
				<h3>{m['caudal.stepDiscover']()}</h3>
				<p>{m['caudal.stepDiscoverCopy']()}</p>
				<a class="text-link" href={resolve('/(public)/events', {})}
					>{m['caudal.explore']()}<ArrowRight size={17} /></a
				>
			</article>
			<article use:reveal>
				<div class="step-top"><span>02</span><Ticket size={28} strokeWidth={1} /></div>
				<h3>{m['caudal.stepTicket']()}</h3>
				<p>{m['caudal.stepTicketCopy']()}</p>
				<a class="text-link" href={resolve('/(auth)/dashboard/tickets', {})}
					>{m['nav.myTickets']()}<ArrowRight size={17} /></a
				>
			</article>
			<article use:reveal>
				<div class="step-top"><span>03</span><QrCode size={28} strokeWidth={1} /></div>
				<h3>{m['caudal.stepEntry']()}</h3>
				<p>{m['caudal.stepEntryCopy']()}</p>
			</article>
		</div>
	</section>

	<ProducerSection />

	<Family />
</div>

<style>
	.caudal-home {
		--gutter: clamp(22px, 4.7vw, 88px);
		overflow: clip;
	}
	.wrap {
		width: min(100%, 1700px);
		margin-inline: auto;
		padding-inline: var(--gutter);
	}
	.hero {
		position: relative;
		min-height: calc(100svh - 88px);
		display: flex;
		flex-direction: column;
		border-bottom: 1px solid hsl(var(--border));
	}
	.flow-field {
		position: absolute;
		inset: 0 0 0 27%;
		mask-image: linear-gradient(90deg, transparent, black 25%);
	}
	.hero-meta {
		position: relative;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 34px;
		gap: 20px;
	}
	.eyebrow {
		font-size: 10px;
		letter-spacing: 0.17em;
		text-transform: uppercase;
		line-height: 1.6;
		font-weight: 500;
		display: flex;
		align-items: center;
		gap: 11px;
	}
	.eyebrow i {
		width: 4px;
		height: 4px;
		border-radius: 50%;
		background: currentColor;
	}
	.location {
		font-size: 9px;
		text-transform: uppercase;
		letter-spacing: 0.14em;
		color: hsl(var(--muted-foreground));
	}
	.hero-body {
		flex: 1;
		display: grid;
		grid-template-columns: 1.5fr 1fr;
		gap: 30px;
		align-items: center;
		padding-block: 90px 100px;
		position: relative;
	}
	.hero-copy {
		position: relative;
		z-index: 1;
	}
	h1 {
		font-family: 'Manrope', sans-serif;
		font-weight: 400;
		font-size: clamp(65px, 8.5vw, 150px);
		line-height: 1.07;
		letter-spacing: -0.075em;
	}
	h1 span {
		display: block;
	}
	.second-line {
		font-family: Georgia, serif;
		font-style: italic;
		font-size: 0.98em;
		letter-spacing: -0.07em;
	}
	.hero-copy > p {
		font-size: 15px;
		line-height: 1.7;
		color: hsl(var(--muted-foreground));
		max-width: 340px;
		margin-top: 30px;
	}
	.hero-actions {
		display: flex;
		gap: 27px;
		align-items: center;
		flex-wrap: wrap;
		margin-top: 30px;
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
	.text-link {
		font-size: 12px;
		display: inline-flex;
		align-items: center;
		gap: 16px;
		padding-block: 10px;
		width: fit-content;
	}
	.text-link :global(svg) {
		transition: transform 0.25s;
	}
	.text-link:hover :global(svg) {
		transform: translate(3px, -2px);
	}
	.hero-object {
		display: flex;
		justify-content: center;
		align-items: center;
		padding-bottom: 20px;
	}
	.hero-bottom {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding-block: 20px 26px;
		gap: 20px;
		font-size: 10px;
		color: hsl(var(--muted-foreground));
	}
	.scroll-link {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.scroll-link > span {
		border: 1px solid hsl(var(--border));
		border-radius: 50%;
		padding: 11px 5px;
	}
	.motion-toggle {
		display: flex;
		align-items: center;
		gap: 7px;
		border: 1px solid hsl(var(--border));
		border-radius: 30px;
		padding: 9px 12px;
		font-size: 9px;
		color: hsl(var(--foreground));
	}
	.motion-toggle:disabled {
		color: hsl(var(--muted-foreground));
	}
	.section-space {
		padding-block: 100px;
		scroll-margin-top: 105px;
	}
	.section-heading {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 30px;
		margin-bottom: 40px;
	}
	h2 {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(35px, 4.2vw, 66px);
		font-weight: 400;
		line-height: 1.14;
		letter-spacing: -0.055em;
		margin-top: 22px;
		max-width: 680px;
	}
	.event-search {
		display: flex;
		align-items: center;
		border-bottom: 1px solid hsl(var(--input));
		gap: 15px;
		padding: 10px 0 16px;
		margin-bottom: 40px;
	}
	.event-search input {
		background: transparent;
		min-width: 0;
		width: 100%;
		font-size: 14px;
		padding: 10px 0;
		border: 0;
	}
	.event-search input::placeholder {
		color: hsl(var(--muted-foreground));
		opacity: 1;
	}
	.event-search button {
		width: 44px;
		height: 44px;
		display: grid;
		place-items: center;
		border: 1px solid hsl(var(--border));
		border-radius: 50%;
		flex-shrink: 0;
		transition: background 0.2s;
	}
	.event-search button:hover {
		background: hsl(var(--secondary));
	}
	.event-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 28px;
	}
	.event-grid.two-events {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
	.event-card {
		min-width: 0;
		display: block;
	}
	.event-art {
		aspect-ratio: 1.45;
		position: relative;
		overflow: hidden;
		background: hsl(var(--poster-paper));
		color: hsl(var(--poster-ink));
	}
	.event-art img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.7s;
	}
	.event-card:hover .event-art img {
		transform: scale(1.04);
	}
	.poster-lines {
		position: absolute;
		width: 120%;
		height: 120%;
		inset: -50% -50% auto auto;
		border: 1px solid currentColor;
		border-radius: 50%;
		box-shadow:
			0 0 0 14px hsl(var(--poster-paper)),
			0 0 0 15px currentColor,
			0 0 0 29px hsl(var(--poster-paper)),
			0 0 0 30px currentColor,
			0 0 0 44px hsl(var(--poster-paper)),
			0 0 0 45px currentColor,
			0 0 0 59px hsl(var(--poster-paper)),
			0 0 0 60px currentColor,
			0 0 0 74px hsl(var(--poster-paper)),
			0 0 0 75px currentColor;
		opacity: 0.22;
		transition: transform 0.7s;
	}
	.event-card:hover .poster-lines {
		transform: translate(-12px, 10px);
	}
	.poster-title {
		position: absolute;
		left: 24px;
		right: 24px;
		bottom: 28px;
		font-family: 'Manrope', sans-serif;
		font-size: clamp(26px, 3.7vw, 56px);
		letter-spacing: -0.065em;
		line-height: 1;
		max-width: 250px;
	}
	.alternate .poster-lines {
		transform: rotate(-90deg);
		inset: auto auto -70% -30%;
	}
	.event-index {
		position: absolute;
		top: 20px;
		left: 24px;
		font-size: 10px;
		letter-spacing: 0.1em;
		background: hsl(var(--poster-paper));
		color: hsl(var(--poster-ink));
		padding: 4px 8px;
	}
	.event-details {
		padding-block: 22px;
		border-bottom: 1px solid hsl(var(--border));
	}
	.event-date {
		color: hsl(var(--muted-foreground));
		font-size: 11px;
		margin-bottom: 12px;
	}
	.event-details h3 {
		font-family: 'Manrope', sans-serif;
		font-size: 21px;
		letter-spacing: -0.035em;
		line-height: 1.35;
	}
	.event-organizer {
		font-size: 12px;
		margin-top: 10px;
		color: hsl(var(--muted-foreground));
	}
	.event-cta {
		display: flex;
		justify-content: space-between;
		font-size: 11px;
		margin-top: 26px;
	}
	.agenda-empty {
		grid-column: 1/-1;
		padding: 45px 0;
		display: flex;
		flex-direction: column;
		gap: 20px;
		color: hsl(var(--muted-foreground));
	}
	.demo-note {
		border-top: 1px solid hsl(var(--border));
		padding-top: 18px;
		margin-top: 28px;
		color: hsl(var(--muted-foreground));
		font-size: 11px;
		line-height: 1.7;
	}
	.marquee {
		overflow: hidden;
		border-block: 1px solid hsl(var(--border));
		padding-block: 22px;
	}
	.marquee-track {
		display: flex;
		width: max-content;
		animation: marquee 40s linear infinite;
	}
	.marquee span {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(35px, 5vw, 75px);
		font-weight: 400;
		letter-spacing: -0.05em;
		padding-right: 25px;
		white-space: nowrap;
	}
	.motion-paused .marquee-track {
		animation-play-state: paused;
	}
	.journey-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 40px;
		margin-top: 60px;
	}
	.journey article {
		border-top: 1px solid hsl(var(--border));
		padding-top: 20px;
	}
	.step-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 45px;
	}
	.step-top span {
		color: hsl(var(--muted-foreground));
		font-size: 11px;
	}
	.journey h3 {
		font-size: 21px;
		font-family: 'Manrope', sans-serif;
		letter-spacing: -0.04em;
	}
	.journey article > p {
		font-size: 13px;
		line-height: 1.8;
		color: hsl(var(--muted-foreground));
		max-width: 280px;
		margin-block: 16px;
	}
	@keyframes marquee {
		to {
			transform: translateX(-25%);
		}
	}
	@media (min-width: 1500px) {
		.hero {
			min-height: 850px;
		}
	}
	@media (max-width: 1023px) {
		.hero-body {
			grid-template-columns: 1.4fr 1fr;
		}
		h1 {
			font-size: 8.5vw;
		}
		.hero-actions {
			gap: 16px;
		}
		.event-grid,
		.event-grid.two-events {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
		.hero-bottom > p {
			display: none;
		}
	}
	@media (max-width: 767px) {
		.hero {
			min-height: auto;
		}
		.hero-meta {
			padding-top: 25px;
		}
		.location {
			display: none;
		}
		.hero-body {
			display: flex;
			flex-direction: column;
			align-items: stretch;
			padding-block: 48px 70px;
			gap: 80px;
		}
		h1 {
			font-size: clamp(44px, 11vw, 85px);
		}
		.hero-copy > p {
			font-size: 14px;
			margin-top: 25px;
			max-width: 300px;
		}
		.hero-actions {
			gap: 20px;
		}
		.pill {
			padding: 16px 20px;
			gap: 20px;
		}
		.hero-object {
			padding-block: 10px 20px;
			justify-content: flex-end;
			padding-right: 12%;
		}
		.flow-field {
			inset: 25% -40% 0 -30%;
		}
		.hero-bottom {
			padding-bottom: 25px;
			gap: 12px;
		}
		.section-space {
			padding-block: 65px;
		}
		.section-heading {
			align-items: flex-start;
			flex-direction: column;
			gap: 14px;
			margin-bottom: 25px;
		}
		h2 {
			font-size: 36px;
		}
		.event-search input {
			font-size: 12px;
		}
		.event-grid,
		.event-grid.two-events {
			grid-template-columns: 1fr;
			gap: 22px;
		}
		.event-art {
			aspect-ratio: 1.6;
		}
		.poster-title {
			font-size: 45px;
			max-width: 230px;
		}
		.journey-grid {
			grid-template-columns: 1fr;
			gap: 30px;
			margin-top: 35px;
		}
		.step-top {
			margin-bottom: 22px;
		}
		.journey article > p {
			max-width: 350px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		*,
		*::before,
		*::after {
			animation: none !important;
			transition: none !important;
			scroll-behavior: auto !important;
		}
	}
</style>
