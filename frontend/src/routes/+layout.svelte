<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import BackButton from '$lib/BackButton.svelte';
	import { page } from '$app/stores';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen bg-gray-50">
	{#if $page.url.pathname !== '/'}
		<div class="p-4">
			<BackButton />
		</div>
	{/if}
	
	{@render children?.()}
</div>
