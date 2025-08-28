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
		},
		{
			title: 'Translation & Interpretation',
			description: 'Get cost estimates for translation and interpretation services',
			path: '/translations',
			icon: '🌐'
		},
		{
			title: 'Catering Estimates',
			description: 'Calculate catering costs for events and meetings',
			path: '/catering',
			icon: '🍽️'
		},
		{
			title: 'Equipment Estimates',
			description: 'Calculate equipment rental and support costs',
			path: '/equipment',
			icon: '💻'
		},
		{
			title: 'Printing Estimates',
			description: 'Calculate printing and production costs',
			path: '/printing',
			icon: '🖨️'
		},
		{
			title: 'Venue Estimates',
			description: 'Calculate venue rental and event service costs',
			path: '/venue',
			icon: '🏢'
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

	<section class="grid grid-cols-1 gap-6 md:grid-cols-3">
		{#each estimateTypes as estimate}
			<button
				class="group rounded-2xl bg-white p-6 shadow transition-all hover:scale-105 hover:shadow-lg"
				onclick={() => navigateTo(estimate.path)}
			>
				<div class="text-center">
					<div class="mb-4 text-4xl">{estimate.icon}</div>
					<h2 class="mb-2 text-xl font-semibold group-hover:text-blue-600">{estimate.title}</h2>
					<p class="text-sm text-gray-600">{estimate.description}</p>
				</div>
			</button>
		{/each}
	</section>

	<footer class="pt-8 text-center text-sm text-gray-500">
		Demo client for travel estimation services
	</footer>
</div>
