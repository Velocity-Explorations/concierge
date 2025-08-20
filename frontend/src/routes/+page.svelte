<script lang="ts">
	import { goto } from '$app/navigation';

	const estimateTypes = [
		{
			title: 'Flight Estimates',
			description: 'Calculate flight costs and find the best options for your travel',
			path: '/flights',
			icon: '✈️'
		},
		{
			title: 'Per-Diem Estimates',
			description: 'Calculate meal and lodging allowances for business travel',
			path: '/per-diem',
			icon: '🏨'
		}
	];

	function navigateTo(path: string) {
		goto(path);
	}
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	<header class="text-center">
		<h1 class="text-3xl font-bold">Travel Estimates</h1>
		<p class="mt-2 text-gray-600">Choose the type of estimate you need</p>
	</header>

	<section class="grid grid-cols-1 gap-6 md:grid-cols-2">
		{#each estimateTypes as estimate}
			<button
				class="group rounded-2xl bg-white p-6 shadow transition-all hover:shadow-lg hover:scale-105"
				onclick={() => navigateTo(estimate.path)}
			>
				<div class="text-center">
					<div class="text-4xl mb-4">{estimate.icon}</div>
					<h2 class="text-xl font-semibold mb-2 group-hover:text-blue-600">{estimate.title}</h2>
					<p class="text-gray-600 text-sm">{estimate.description}</p>
				</div>
			</button>
		{/each}
	</section>

	<footer class="text-center text-sm text-gray-500 pt-8">
		Demo client for travel estimation services
	</footer>
</div>
