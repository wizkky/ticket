<script lang="ts">
	import { mode, setMode, userPrefersMode } from 'mode-watcher';
	import { Sun, Moon, Monitor } from '@lucide/svelte';
	import * as Dropdown from '$lib/components/ui/dropdown-menu';
	import * as m from '$lib/paraglide/messages.js';
	const themes = $derived([
		{ value: 'light' as const, label: m['theme.light'](), icon: Sun },
		{ value: 'dark' as const, label: m['theme.dark'](), icon: Moon },
		{ value: 'system' as const, label: m['theme.system'](), icon: Monitor }
	]);
	function choose(value: string) {
		if (value === 'light' || value === 'dark' || value === 'system') setMode(value);
	}
</script>

<Dropdown.Root>
	<Dropdown.Trigger
		class="inline-flex min-h-11 min-w-11 items-center justify-center rounded-full text-muted-foreground transition-colors hover:bg-accent hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
		aria-label={m['theme.toggleTheme']()}
	>
		{#if mode.current === 'light'}<Sun size={20} />{:else if mode.current === 'dark'}<Moon
				size={20}
			/>{:else}<Monitor size={20} />{/if}
	</Dropdown.Trigger>
	<Dropdown.Content align="end">
		<Dropdown.RadioGroup value={userPrefersMode.current} onValueChange={choose}>
			{#each themes as theme (theme.value)}{@const Icon = theme.icon}<Dropdown.RadioItem
					value={theme.value}
					class="min-h-11 gap-3"><Icon size={16} />{theme.label}</Dropdown.RadioItem
				>{/each}
		</Dropdown.RadioGroup>
	</Dropdown.Content>
</Dropdown.Root>
