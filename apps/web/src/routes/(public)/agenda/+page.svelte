<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, CalendarDays, Repeat2, Users, Clock3 } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<svelte:head
	><title>Caudal Agenda · Caudal Creativo</title><meta
		name="description"
		content={m['creative.agendaIntro']()}
	/><meta name="robots" content="noindex,nofollow" /></svelte:head
>

<section class="creative-section agenda-hero" aria-labelledby="agenda-title">
	<div class="hero-meta">
		<p class="creative-eyebrow">Caudal Creativo / Caudal Agenda</p>
		<span class="creative-status pending">{m['creative.development']()}</span>
	</div>
	<h1 id="agenda-title" class="creative-title">{m['creative.agendaTitle']()}</h1>
	<p class="creative-intro">{m['creative.agendaIntro']()}</p>
	<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- the route is resolved before appending calendar query parameters -->
	<a class="creative-pill" href={`${resolve('/(public)/events', {})}?viewMode=calendar`}
		>{m['creative.openCalendar']()}<ArrowUpRight size={20} aria-hidden="true" /></a
	>
	<div class="calendar-art" aria-hidden="true"><CalendarDays size="100%" strokeWidth={0.4} /></div>
</section>
<section class="creative-section calendar-live" aria-labelledby="calendar-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">{m['creative.available']()}</p>
			<h2 id="calendar-title">{m['creative.calendarLive']()}</h2>
		</div>
		<p>{m['creative.calendarCopy']()}</p>
	</div>
	<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- the route is resolved before appending calendar query parameters -->
	<a class="creative-link" href={`${resolve('/(public)/events', {})}?viewMode=calendar`}
		>{m['creative.openCalendar']()}<ArrowUpRight size={18} aria-hidden="true" /></a
	>
</section>
<section class="creative-section" aria-labelledby="future-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">{m['creative.development']()}</p>
			<h2 id="future-title">{m['creative.futureTitle']()}</h2>
		</div>
	</div>
	<div class="future-grid">
		<article>
			<Repeat2 size={28} strokeWidth={1} aria-hidden="true" />
			<h3>{m['creative.recurrence']()}</h3>
			<span class="creative-status pending">{m['creative.development']()}</span>
		</article>
		<article>
			<Users size={28} strokeWidth={1} aria-hidden="true" />
			<h3>{m['creative.students']()}</h3>
			<span class="creative-status pending">{m['creative.development']()}</span>
		</article>
		<article>
			<Clock3 size={28} strokeWidth={1} aria-hidden="true" />
			<h3>{m['creative.appointments']()}</h3>
			<span class="creative-status pending">{m['creative.development']()}</span>
		</article>
	</div>
	<p class="creative-intro">{m['creative.futureCopy']()}</p>
</section>

<style>
	.agenda-hero {
		position: relative;
		overflow: hidden;
		border-bottom: 1px solid hsl(var(--border));
	}
	.hero-meta {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 20px;
	}
	.creative-title {
		max-width: 800px;
		position: relative;
		z-index: 1;
	}
	.calendar-art {
		width: 360px;
		height: 360px;
		position: absolute;
		right: 6%;
		bottom: 0;
		transform: rotate(-12deg);
		opacity: 0.13;
		pointer-events: none;
	}
	.calendar-live {
		background: hsl(var(--card));
		border-bottom: 1px solid hsl(var(--border));
	}
	.future-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		border-block: 1px solid hsl(var(--border));
	}
	article {
		padding: 32px;
		border-right: 1px solid hsl(var(--border));
	}
	article:first-child {
		padding-left: 0;
	}
	article:last-child {
		border-right: 0;
	}
	h3 {
		font-size: 25px;
		font-weight: 400;
		letter-spacing: -0.04em;
		line-height: 1.25;
		margin-block: 28px;
	}
	@media (max-width: 767px) {
		.hero-meta {
			align-items: start;
			flex-direction: column;
		}
		.calendar-art {
			display: none;
		}
		.future-grid {
			grid-template-columns: 1fr;
		}
		article,
		article:first-child {
			padding: 26px 0;
			border-right: 0;
			border-bottom: 1px solid hsl(var(--border));
		}
		article:last-child {
			border-bottom: 0;
		}
	}
</style>
