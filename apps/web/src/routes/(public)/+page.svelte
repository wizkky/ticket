<script lang="ts">
	import { resolve } from '$app/paths';
	import { CalendarDays, QrCode, Users } from '@lucide/svelte';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import { authStore } from '$lib/stores/auth.svelte';

	const isAuthenticated = $derived(authStore.isAuthenticated);
</script>

<svelte:head>
	<title>{m['caudal.metaTitle']()}</title>
	<meta name="description" content={m['caudal.intro']()} />
	<meta name="robots" content="noindex,nofollow" />
</svelte:head>

<section class="border-b bg-secondary text-secondary-foreground">
	<div class="container mx-auto max-w-5xl px-4 py-14 sm:py-20">
		<PageHeader
			volume="poster"
			onBand
			kicker={m['caudal.badge']()}
			title={m['caudal.title']()}
			subtitle={m['caudal.intro']()}
		/>
		<div class="mt-8 flex flex-wrap gap-3">
			<a
				href={resolve('/(public)/events', {})}
				class="rounded-md bg-primary px-6 py-3 font-bold text-primary-foreground transition-colors hover:bg-primary/90"
			>
				{m['nav.browseEvents']()}
			</a>
			<a
				href={isAuthenticated ? resolve('/(auth)/dashboard', {}) : resolve('/(public)/login', {})}
				class="rounded-md border border-border bg-background px-6 py-3 font-bold text-foreground transition-colors hover:bg-muted"
			>
				{isAuthenticated ? m['caudal.dashboard']() : m['auth.login']()}
			</a>
		</div>
	</div>
</section>

<section class="container mx-auto max-w-5xl px-4 py-10 sm:py-14">
	<div class="grid gap-5 md:grid-cols-3">
		<article class="rounded-xl border bg-card p-6 text-card-foreground">
			<CalendarDays class="mb-4 h-7 w-7 text-primary" aria-hidden="true" />
			<h2 class="text-xl font-extrabold">{m['caudal.eventsTitle']()}</h2>
			<p class="mt-3 text-muted-foreground">{m['caudal.eventsDescription']()}</p>
			<a
				href={resolve('/(public)/events', {})}
				class="mt-5 inline-block font-bold underline underline-offset-4"
			>
				{m['nav.browseEvents']()}
			</a>
		</article>
		<article class="rounded-xl border bg-card p-6 text-card-foreground">
			<Users class="mb-4 h-7 w-7 text-primary" aria-hidden="true" />
			<h2 class="text-xl font-extrabold">{m['caudal.producersTitle']()}</h2>
			<p class="mt-3 text-muted-foreground">{m['caudal.producersDescription']()}</p>
			<a
				href={resolve('/(public)/organizations', {})}
				class="mt-5 inline-block font-bold underline underline-offset-4"
			>
				{m['nav.organizations']()}
			</a>
		</article>
		<article class="rounded-xl border bg-card p-6 text-card-foreground">
			<QrCode class="mb-4 h-7 w-7 text-primary" aria-hidden="true" />
			<h2 class="text-xl font-extrabold">{m['caudal.ticketsTitle']()}</h2>
			<p class="mt-3 text-muted-foreground">{m['caudal.ticketsDescription']()}</p>
			<a
				href={resolve('/(auth)/dashboard/tickets', {})}
				class="mt-5 inline-block font-bold underline underline-offset-4"
			>
				{m['nav.myTickets']()}
			</a>
		</article>
	</div>
	<p class="mt-8 rounded-xl border bg-muted p-5 text-sm text-muted-foreground">
		{m['caudal.paymentNote']()}
	</p>
</section>
