<script lang="ts">
	import { ArrowUpRight, Asterisk } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
	interface Props {
		paused: boolean;
	}
	const { paused }: Props = $props();
</script>

<!-- A typographic brand object, not a purchasable or scannable ticket. -->
<div class="ticket-orbit" class:paused aria-hidden="true">
	<div class="orbit-label">{m['caudal.visualCaption']()}</div>
	<div class="paper">
		<div class="ticket-top">
			<!-- i18n-ignore: brand name --><span>CAUDAL TICKETS</span><ArrowUpRight
				size={20}
				strokeWidth={1}
			/>
		</div>
		<div class="ticket-type">
			{m['caudal.ticketLineOne']()}<br /><span>{m['caudal.ticketLineTwo']()}</span>
		</div>
		<div class="ticket-art">
			<div></div>
			<div></div>
			<div></div>
		</div>
		<div class="ticket-bottom">
			<span>{m['caudal.ticketCaption']()}</span><span class="ticket-star"
				><Asterisk size="1em" strokeWidth={1} /></span
			>
		</div>
		<div class="stub"><span>{m['caudal.ticketStub']()}</span><span class="barcode"></span></div>
	</div>
	<div class="coordinate"><span>39° S / 73° O</span><span>↗</span></div>
</div>

<style>
	.ticket-orbit {
		position: relative;
		width: clamp(220px, 23vw, 340px);
		animation: float 9s ease-in-out infinite;
	}
	.orbit-label {
		position: absolute;
		top: -42px;
		right: 0;
		font-size: 9px;
		letter-spacing: 0.2em;
		text-transform: uppercase;
		color: hsl(var(--muted-foreground));
	}
	.paper {
		color: hsl(var(--poster-ink));
		background: hsl(var(--poster-paper));
		transform: rotate(9deg);
		box-shadow: 0 22px 80px hsl(var(--poster-ink) / 0.2);
		position: relative;
	}
	.paper::before,
	.paper::after {
		content: '';
		position: absolute;
		width: 20px;
		height: 20px;
		bottom: 57px;
		border-radius: 50%;
		background: hsl(var(--background));
		z-index: 2;
	}
	.paper::before {
		left: -10px;
	}
	.paper::after {
		right: -10px;
	}
	.ticket-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 0 22px;
		padding: 21px 0 16px;
		border-bottom: 1px solid hsl(var(--poster-ink) / 0.25);
		font-size: 9px;
		letter-spacing: 0.18em;
	}
	.ticket-type {
		padding: 22px 22px 0;
		font-family: 'Manrope', sans-serif;
		font-size: clamp(35px, 3.4vw, 50px);
		line-height: 1.07;
		letter-spacing: -0.065em;
		font-weight: 500;
	}
	.ticket-type span {
		font-family: Georgia, serif;
		font-style: italic;
		font-weight: 400;
	}
	.ticket-art {
		height: 135px;
		position: relative;
		overflow: hidden;
		margin: 20px 22px;
	}
	.ticket-art div {
		position: absolute;
		width: 185px;
		height: 185px;
		border: 1px solid hsl(var(--poster-ink) / 0.4);
		border-radius: 50%;
		box-shadow:
			0 0 0 5px hsl(var(--poster-paper)),
			0 0 0 6px hsl(var(--poster-ink) / 0.25),
			0 0 0 11px hsl(var(--poster-paper)),
			0 0 0 12px hsl(var(--poster-ink) / 0.25),
			0 0 0 17px hsl(var(--poster-paper)),
			0 0 0 18px hsl(var(--poster-ink) / 0.25),
			0 0 0 23px hsl(var(--poster-paper)),
			0 0 0 24px hsl(var(--poster-ink) / 0.25);
		top: 36px;
		left: -85px;
	}
	.ticket-art div:nth-child(2) {
		left: 50px;
		top: -145px;
	}
	.ticket-art div:nth-child(3) {
		left: 165px;
		top: 56px;
	}
	.ticket-bottom {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 22px 16px;
		gap: 25px;
	}
	.ticket-bottom > span:first-child {
		font-size: 9px;
		text-transform: uppercase;
		letter-spacing: 0.14em;
		max-width: 150px;
	}
	.ticket-star {
		font-size: 35px;
	}
	.stub {
		border-top: 1px dashed hsl(var(--poster-ink) / 0.45);
		height: 67px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 22px;
		gap: 20px;
	}
	.stub > span:first-child {
		font-size: 9px;
		letter-spacing: 0.15em;
		text-transform: uppercase;
	}
	.barcode {
		width: 75px;
		height: 24px;
		flex-shrink: 0;
		background: repeating-linear-gradient(
			90deg,
			hsl(var(--poster-ink)) 0 1px,
			transparent 1px 3px,
			hsl(var(--poster-ink)) 3px 6px,
			transparent 6px 8px,
			hsl(var(--poster-ink)) 8px 9px,
			transparent 9px 13px
		);
	}
	.coordinate {
		display: flex;
		justify-content: space-between;
		position: absolute;
		width: 100%;
		bottom: -73px;
		font-size: 9px;
		letter-spacing: 0.18em;
		color: hsl(var(--muted-foreground));
	}
	.coordinate span:last-child {
		font-size: 28px;
	}
	.paused {
		animation-play-state: paused;
	}
	@keyframes float {
		0%,
		100% {
			transform: translateY(0) rotate(-2deg);
		}
		50% {
			transform: translateY(-16px) rotate(1deg);
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.ticket-orbit {
			animation: none;
		}
	}
	@media (max-width: 767px) {
		.ticket-orbit {
			width: 210px;
		}
		.ticket-top {
			padding: 14px 0;
		}
		.ticket-type {
			font-size: 32px;
			padding-top: 16px;
		}
		.ticket-art {
			height: 90px;
			margin: 18px 22px;
		}
		.coordinate {
			bottom: -56px;
		}
	}
</style>
