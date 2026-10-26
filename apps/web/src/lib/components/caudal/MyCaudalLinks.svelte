<script lang="ts">
	import { resolve } from '$app/paths';
	import { Ticket, CalendarDays, Heart, BookmarkCheck, ArrowUpRight } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
	const { hasActivities = false }: { hasActivities?: boolean } = $props();
</script>

<section class="my-caudal" aria-labelledby="my-caudal-title">
	<h2 id="my-caudal-title">{m['creative.myCaudal']()}</h2>
	<p>{m['creative.myIntro']()}</p>
	<nav aria-label={m['creative.myCaudal']()}>
		<a href={resolve('/(auth)/dashboard/tickets', {})}
			><Ticket size={20} strokeWidth={1.2} aria-hidden="true" /><span>{m['nav.myTickets']()}</span
			><ArrowUpRight size={16} aria-hidden="true" /></a
		>
		<a href={resolve('/(auth)/dashboard/rsvps', {})}
			><BookmarkCheck size={20} strokeWidth={1.2} aria-hidden="true" /><span
				>{m['nav.rsvps']()}</span
			><ArrowUpRight size={16} aria-hidden="true" /></a
		>
		<a href={resolve('/(auth)/dashboard/following', {})}
			><Heart size={20} strokeWidth={1.2} aria-hidden="true" /><span
				>{m['dashboard.following.title']()}</span
			><ArrowUpRight size={16} aria-hidden="true" /></a
		>
		<!-- eslint-disable svelte/no-navigation-without-resolve -- both destinations are resolved before appending calendar state -->
		<a
			href={hasActivities
				? `${resolve('/(auth)/dashboard', {})}?viewMode=calendar#your-events-heading`
				: `${resolve('/(public)/events', {})}?viewMode=calendar`}
			><CalendarDays size={20} strokeWidth={1.2} aria-hidden="true" /><span
				>{m['creative.openCalendar']()}</span
			><ArrowUpRight size={16} aria-hidden="true" /></a
		>
		<!-- eslint-enable svelte/no-navigation-without-resolve -->
	</nav>
	<p class="future">
		{m['creative.myFuture']()}
		<a href={resolve('/(public)/agenda', {})}>{m['creative.learnAgenda']()}</a>
	</p>
</section>

<style>
	.my-caudal {
		background: hsl(var(--card));
		border: 1px solid hsl(var(--border));
		padding: 28px;
		margin-bottom: 30px;
	}
	h2 {
		font-size: 30px;
		font-weight: 400;
		letter-spacing: -0.045em;
	}
	p {
		font-size: 13px;
		color: hsl(var(--muted-foreground));
		line-height: 1.8;
		margin-top: 12px;
	}
	nav {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		margin-top: 24px;
		gap: 10px;
	}
	nav a {
		display: flex;
		align-items: center;
		gap: 12px;
		border: 1px solid hsl(var(--border));
		padding: 18px 14px;
		font-size: 12px;
	}
	nav a:hover {
		background: hsl(var(--muted));
	}
	nav span {
		flex: 1;
	}
	nav :global(svg) {
		flex-shrink: 0;
	}
	.future {
		margin-top: 22px;
		font-size: 11px;
	}
	.future a {
		text-decoration: underline;
		text-underline-offset: 3px;
	}
	@media (max-width: 1023px) {
		nav {
			grid-template-columns: 1fr 1fr;
		}
	}
	@media (max-width: 479px) {
		.my-caudal {
			padding: 22px 18px;
		}
		nav {
			grid-template-columns: 1fr;
		}
	}
</style>
