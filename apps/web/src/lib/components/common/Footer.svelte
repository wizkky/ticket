<script lang="ts">
	import RevelWordmark from '$lib/components/brand/RevelWordmark.svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<footer class="border-t bg-card text-card-foreground">
	<div
		class="container mx-auto flex max-w-5xl flex-col gap-5 px-4 py-8 sm:flex-row sm:items-center sm:justify-between"
	>
		<div>
			<RevelWordmark />
			<p class="mt-3 text-sm text-muted-foreground">
				{m['caudal.footerBasis']()}
				<!-- i18n-ignore: upstream product and license names -->
				<a href="https://github.com/letsrevel/revel-backend" class="underline underline-offset-4"
					>Revel (MIT)</a
				>
			</p>
		</div>
		<!-- i18n-ignore: repository name -->
		<a
			href="https://github.com/wizkky/ticket"
			class="text-sm font-semibold underline underline-offset-4">GitHub · CaudalTickets</a
		>
	</div>
</footer>
