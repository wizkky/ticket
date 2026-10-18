<script lang="ts">
	import type { Snippet } from 'svelte';
	import PageHeader from '$lib/components/common/PageHeader.svelte';

	interface Props {
		/** Already-translated strings — i18n stays at the call site. */
		title: string;
		kicker?: string;
		subtitle?: string;
		/** Right-aligned on sm+, same slot PageHeader exposes. */
		actions?: Snippet;
		children: Snippet;
	}
	const { title, kicker, subtitle, actions, children }: Props = $props();
</script>

<div class="bg-background">
	<section class="border-b text-foreground">
		<div class="container mx-auto px-4 pb-12 pt-10 md:pt-14">
			<PageHeader volume="poster" {kicker} {title} {subtitle} {actions} />
		</div>
	</section>

	<div class="container mx-auto px-4 pb-8 pt-8 md:pb-12">
		{@render children()}
	</div>
</div>
