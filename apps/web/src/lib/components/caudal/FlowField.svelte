<script lang="ts">
	import { onMount } from 'svelte';
	interface Props {
		paused: boolean;
	}
	const { paused }: Props = $props();
	let canvas: HTMLCanvasElement;
	let render = () => {
		/* initialized on mount */
	};
	$effect(() => {
		void paused;
		render();
	});

	onMount(() => {
		const ctx = canvas.getContext('2d');
		if (!ctx) return;
		const motion = matchMedia('(prefers-reduced-motion: reduce)');
		let frame = 0,
			width = 1,
			height = 1,
			time = 0,
			last = 0;
		let visible = true,
			pointer = 0,
			target = 0;
		const draw = (now = 0) => {
			frame = 0;
			const moving = !paused && !motion.matches && visible && !document.hidden;
			if (moving && last) time += Math.min(now - last, 50) * 0.00015;
			last = moving ? now : 0;
			pointer += (target - pointer) * 0.035;
			ctx.clearRect(0, 0, width, height);
			ctx.save();
			ctx.scale(width / 1000, height / 900);
			const ink = getComputedStyle(canvas).color;
			ctx.strokeStyle = ink;
			for (let bank = 0; bank < 3; bank++) {
				for (let line = 0; line < 32; line++) {
					const offset = line * 4.5;
					const wave = Math.sin(time + line * 0.065 + bank) * 16 + pointer * 24;
					ctx.globalAlpha = 0.075 + (line % 7 === 0 ? 0.13 : 0);
					ctx.lineWidth = line % 7 === 0 ? 0.9 : 0.65;
					ctx.beginPath();
					if (bank === 0) {
						ctx.moveTo(160 + offset, -80);
						ctx.bezierCurveTo(30 + offset, 250, 880 + wave, 220, 580 + offset * 0.7, 580);
					} else if (bank === 1) {
						ctx.moveTo(1030, 90 + offset);
						ctx.bezierCurveTo(590, 180 + offset, 430 + wave, 390, 580 + offset * 0.7, 580);
					} else {
						ctx.moveTo(1100, 550 + offset);
						ctx.bezierCurveTo(800, 350 + offset, 430 + wave, 380, 580 + offset * 0.7, 580);
					}
					ctx.bezierCurveTo(
						400 + offset * 0.5 + wave,
						740,
						810 + offset,
						750,
						700 + offset * 0.8,
						1000
					);
					ctx.stroke();
				}
			}
			ctx.globalAlpha = 0.5;
			for (let dot = 0; dot < 12; dot++) {
				const phase = (dot / 12 + time * 0.06) % 1;
				const x = 590 + Math.sin(phase * Math.PI * 2 + time) * 210;
				const y = phase * 1000;
				ctx.fillStyle = ink;
				ctx.beginPath();
				ctx.arc(x, y, 1.4, 0, Math.PI * 2);
				ctx.fill();
			}
			ctx.restore();
			if (moving) frame = requestAnimationFrame(draw);
		};
		const schedule = () => {
			if (frame) cancelAnimationFrame(frame);
			last = 0;
			draw();
		};
		render = schedule;
		const resize = new ResizeObserver(([entry]) => {
			width = entry.contentRect.width;
			height = entry.contentRect.height;
			const ratio = Math.min(devicePixelRatio || 1, 2);
			canvas.width = Math.round(width * ratio);
			canvas.height = Math.round(height * ratio);
			ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
			schedule();
		});
		resize.observe(canvas);
		const intersection = new IntersectionObserver(([entry]) => {
			visible = entry.isIntersecting;
			schedule();
		});
		intersection.observe(canvas);
		const theme = new MutationObserver(schedule);
		theme.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
		const move = (event: PointerEvent) => {
			target = event.clientX / innerWidth - 0.5;
		};
		window.addEventListener('pointermove', move, { passive: true });
		document.addEventListener('visibilitychange', schedule);
		motion.addEventListener('change', schedule);
		return () => {
			cancelAnimationFrame(frame);
			resize.disconnect();
			intersection.disconnect();
			theme.disconnect();
			window.removeEventListener('pointermove', move);
			document.removeEventListener('visibilitychange', schedule);
			motion.removeEventListener('change', schedule);
			render = () => {
				/* component disposed */
			};
		};
	});
</script>

<canvas bind:this={canvas} aria-hidden="true"></canvas>

<style>
	canvas {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		color: hsl(var(--foreground));
		pointer-events: none;
	}
</style>
