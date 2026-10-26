<script lang="ts">
	import MotionToggle from '$lib/components/caudal/MotionToggle.svelte';
	import { resolve } from '$app/paths';
	import { ArrowUpRight } from '@lucide/svelte';
	import RevelWordmark from '$lib/components/brand/RevelWordmark.svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<footer class="caudal-footer">
	<div class="footer-top">
		<a href={resolve('/(public)', {})}><RevelWordmark class="text-3xl" /></a>
		<p>{m['creative.heroOne']()}</p>
		<a href="https://www.instagram.com/caudalcreativocl/"
			>{m['caudal.followCaudal']()}<ArrowUpRight size={18} strokeWidth={1.5} /></a
		>
	</div>
	<nav class="footer-links" aria-label={m['creative.ecosystem']()}>
		<a href={resolve('/(public)/events', {})}>{m['creative.explore']()}</a>
		<a href={resolve('/(public)/agenda', {})}>{m['creative.agenda']()}</a>
		<a href={resolve('/(public)/comunidad', {})}>{m['creative.community']()}</a>
		<a href={resolve('/(public)/ecosistema', {})}>{m['creative.ecosystem']()}</a>
		<!-- i18n-ignore: service name --><a href={resolve('/(public)/tickets', {})}>Caudal Tickets</a>
		<a href={resolve('/(auth)/dashboard', {})}>{m['creative.myCaudal']()}</a>
	</nav>
	<div class="mx-auto flex max-w-[1524px] justify-end pb-4"><MotionToggle /></div>
	<div class="footer-bottom">
		<p>{m['caudal.footerOrigin']()}</p>
		<p>
			{m['caudal.footerBasis']()}
			<!-- i18n-ignore: upstream product and license name -->
			<a href="https://github.com/letsrevel/revel-backend">Revel (MIT)</a>
		</p>
		<!-- i18n-ignore: repository name --><a href="https://github.com/wizkky/ticket">GitHub ↗</a>
	</div>
</footer>

<style>
	.caudal-footer {
		border-top: 1px solid hsl(var(--border));
		padding: 50px clamp(22px, 4.7vw, 88px) 25px;
	}
	.footer-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 35px;
		max-width: 1524px;
		margin: auto;
	}
	.footer-top > p {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(25px, 3vw, 45px);
		letter-spacing: -0.05em;
	}
	.footer-top > a:last-child {
		display: flex;
		align-items: center;
		gap: 15px;
		font-size: 12px;
	}
	.footer-links {
		display: flex;
		gap: 30px;
		margin: 40px auto;
		font-size: 12px;
		max-width: 1524px;
	}
	.footer-bottom {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 15px;
		padding-top: 22px;
		border-top: 1px solid hsl(var(--border));
		max-width: 1524px;
		margin: auto;
		font-size: 10px;
		color: hsl(var(--muted-foreground));
		line-height: 1.7;
	}
	.footer-bottom p a {
		text-decoration: underline;
		text-underline-offset: 3px;
	}
	@media (max-width: 767px) {
		.footer-top {
			flex-direction: column;
			align-items: flex-start;
			gap: 25px;
		}
		.footer-links {
			gap: 20px;
			flex-wrap: wrap;
		}
		.footer-bottom {
			flex-direction: column;
		}
	}
</style>
