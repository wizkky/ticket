/** Enhance visible server-rendered content; never hide content before JS starts. */
export function reveal(node: HTMLElement) {
	const motion = matchMedia('(prefers-reduced-motion: reduce)');
	let animation: Animation | undefined;
	const observer = new IntersectionObserver(
		([entry]) => {
			if (entry.isIntersecting) {
				if (!motion.matches && !node.closest('.motion-paused'))
					animation = node.animate(
						[
							{ opacity: 0.3, transform: 'translateY(28px)' },
							{ opacity: 1, transform: 'translateY(0)' }
						],
						{ duration: 750, easing: 'cubic-bezier(.2,.7,.2,1)' }
					);
				observer.disconnect();
			}
		},
		{ threshold: 0.08 }
	);
	observer.observe(node);
	const stop = () => {
		if (motion.matches) animation?.finish();
	};
	const pause = () => animation?.finish();
	motion.addEventListener('change', stop);
	window.addEventListener('caudal-motion-paused', pause);
	return {
		destroy() {
			observer.disconnect();
			animation?.cancel();
			motion.removeEventListener('change', stop);
			window.removeEventListener('caudal-motion-paused', pause);
		}
	};
}
