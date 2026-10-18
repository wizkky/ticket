<script lang="ts">
	import { asset } from '$app/paths';
	import { ArrowUpRight } from '@lucide/svelte';
	import { reveal } from './reveal';
	import * as m from '$lib/paraglide/messages.js';
	// User supplied brand names retain their spelling in every locale.
	const brands = {
		creative: 'Caudal Creativo',
		factoria: 'La Factoría',
		subte: 'El Subte',
		emergia: 'Emergia'
	};
</script>

<section class="family" aria-labelledby="family-title">
	<div class="family-heading" use:reveal>
		<p class="eyebrow">{m['caudal.familyLabel']()}</p>
		<div class="family-intro">
			<h2 id="family-title">{m['caudal.familyTitle']()}</h2>
			<p>{m['caudal.familyCopy']()}</p>
		</div>
	</div>
	<div class="family-grid" use:reveal>
		<div class="parent">
			<img
				src={asset('/brand/caudal/creative.png')}
				alt={brands.creative}
				width="2048"
				height="682"
				loading="lazy"
			/>
		</div>
		<div class="sister">
			<img
				src={asset('/brand/caudal/factoria.png')}
				alt={brands.factoria}
				width="968"
				height="946"
				loading="lazy"
			/>
			<p>{m['caudal.craft']()}</p>
		</div>
		<div class="sister subte">
			<img
				src={asset('/brand/caudal/subte.png')}
				alt={brands.subte}
				width="1254"
				height="1254"
				loading="lazy"
			/>
			<p>{m['caudal.culture']()}</p>
		</div>
		<div class="sister emergia">
			<img
				src={asset('/brand/caudal/emergia.png')}
				alt={brands.emergia}
				width="1254"
				height="1254"
				loading="lazy"
			/>
			<p>{m['caudal.innovation']()}</p>
		</div>
	</div>
	<a class="family-link" href="https://www.instagram.com/caudalcreativocl/"
		>{m['caudal.followCaudal']()}<ArrowUpRight size={18} strokeWidth={1.5} /></a
	>
</section>

<style>
	.family {
		padding: 90px clamp(22px, 4.7vw, 88px);
		width: min(100%, 1700px);
		margin-inline: auto;
	}
	.eyebrow {
		font-size: 10px;
		text-transform: uppercase;
		letter-spacing: 0.17em;
	}
	.family-intro {
		display: grid;
		grid-template-columns: 1.3fr 1fr;
		gap: 100px;
		align-items: end;
		margin-top: 22px;
	}
	h2 {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(35px, 4.2vw, 65px);
		font-weight: 400;
		line-height: 1.15;
		letter-spacing: -0.055em;
		max-width: 700px;
	}
	.family-intro > p {
		font-size: 13px;
		color: hsl(var(--muted-foreground));
		line-height: 1.8;
		max-width: 350px;
	}
	.family-grid {
		display: grid;
		grid-template-columns: 1.25fr 1fr 1fr 1fr;
		margin-top: 60px;
		border-block: 1px solid hsl(var(--border));
	}
	.family-grid > div {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		min-width: 0;
		padding: 30px;
		border-right: 1px solid hsl(var(--border));
	}
	.family-grid > div:last-child {
		border-right: 0;
	}
	.family-grid img {
		width: 100%;
		height: 120px;
		object-fit: contain;
		filter: invert(1);
		mix-blend-mode: multiply;
	}
	:global(.dark) .family-grid img {
		filter: none;
		mix-blend-mode: screen;
	}
	.family-grid .parent {
		padding: 20px;
	}
	.family-grid .parent img {
		height: auto;
	}
	.sister p {
		font-size: 10px;
		color: hsl(var(--muted-foreground));
		margin-top: 17px;
		text-align: center;
	}
	.family-link {
		display: flex;
		align-items: center;
		gap: 20px;
		font-size: 12px;
		width: fit-content;
		padding-block: 20px;
	}
	@media (max-width: 767px) {
		.family {
			padding-block: 65px;
		}
		.family-intro {
			grid-template-columns: 1fr;
			gap: 25px;
		}
		.family-grid {
			grid-template-columns: 1fr 1fr;
			margin-top: 35px;
		}
		.family-grid > div {
			padding: 24px 20px;
			border-bottom: 1px solid hsl(var(--border));
		}
		.family-grid > div:nth-child(2) {
			border-right: 0;
		}
		.family-grid > div:nth-child(n + 3) {
			border-bottom: 0;
		}
		.family-grid .parent {
			padding: 10px;
		}
	}
</style>
