<script lang="ts">
	import { findCateringApiEstimatesCateringPost } from '../../client/sdk.gen';
	import type { CateringModel } from '../../client/types.gen';

	type CateringDataType = Array<CateringModel>;
	type MealType = CateringModel['meal_type'];

	const MEAL_TYPES: MealType[] = ['breakfast', 'lunch', 'dinner'];

	let catering_data = $state<CateringDataType>([]);

	let tempCateringData = $state<Partial<CateringModel>>({
		location: 'San Francisco, CA',
		meals: 10,
		coffee_break: false,
		setup: false,
		clean_up: false,
		delivery: false,
		supplies: false,
		onsite_support: false
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addCateringItem() {
		if (!tempCateringData.meal_type || !tempCateringData.location || !tempCateringData.meals) return;

		const newItem: CateringModel = {
			meal_type: tempCateringData.meal_type,
			location: tempCateringData.location,
			meals: tempCateringData.meals,
			coffee_break: tempCateringData.coffee_break ?? false,
			setup: tempCateringData.setup ?? false,
			clean_up: tempCateringData.clean_up ?? false,
			delivery: tempCateringData.delivery ?? false,
			supplies: tempCateringData.supplies ?? false,
			onsite_support: tempCateringData.onsite_support ?? false
		};

		catering_data = [...catering_data, newItem];

		// Reset form but keep location
		tempCateringData = {
			meal_type: undefined,
			location: tempCateringData.location,
			meals: 10,
			coffee_break: false,
			setup: false,
			clean_up: false,
			delivery: false,
			supplies: false,
			onsite_support: false
		};
	}

	function removeCateringItem(idx: number) {
		catering_data = catering_data.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findCateringApiEstimatesCateringPost({
				body: { catering_data }
			});
		} catch (e: unknown) {
			errorMsg =
				(e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="mx-auto max-w-3xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Catering Estimates</h1>
		<div class="text-sm text-gray-500">Demo client</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add catering item</h2>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			<label class="block text-sm font-medium"
				>Location
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempCateringData.location}
					placeholder="e.g. San Francisco, CA"
				/>
			</label>
			<label class="block text-sm font-medium"
				>Number of meals
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="1"
					bind:value={tempCateringData.meals}
				/>
			</label>
		</div>

		<div class="space-y-3 rounded-xl border bg-gray-50 p-4">
			<h3 class="text-sm font-medium">Meal type</h3>
			<div class="flex flex-wrap gap-2">
				{#each MEAL_TYPES as item (item)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={tempCateringData.meal_type} value={item} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={tempCateringData.meal_type === item}
							class:!text-white={tempCateringData.meal_type === item}
							class:!border-black={tempCateringData.meal_type === item}>{item}</span
						>
					</label>
				{/each}
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.coffee_break} />
				<span class="text-sm">Coffee break</span>
			</label>
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.setup} />
				<span class="text-sm">Setup required</span>
			</label>
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.clean_up} />
				<span class="text-sm">Clean up</span>
			</label>
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.delivery} />
				<span class="text-sm">Delivery</span>
			</label>
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.supplies} />
				<span class="text-sm">Supplies</span>
			</label>
			<label class="inline-flex items-center gap-2">
				<input type="checkbox" bind:checked={tempCateringData.onsite_support} />
				<span class="text-sm">Onsite support</span>
			</label>
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addCateringItem}
				disabled={!tempCateringData.meal_type || !tempCateringData.location || !tempCateringData.meals}
			>
				Add item
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (catering_data = [])}
				disabled={!catering_data.length}
			>
				Clear all
			</button>
		</div>

		{#if catering_data.length}
			<ul class="divide-y rounded-xl border">
				{#each catering_data as item, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{item.meal_type.charAt(0).toUpperCase() + item.meal_type.slice(1)} in {item.location}
							</div>
							<div class="text-gray-500">{item.meals} meal(s)</div>
							<div class="mt-1 text-xs text-gray-500">
								{#if item.coffee_break}Coffee break · {/if}
								{#if item.setup}Setup · {/if}
								{#if item.clean_up}Clean up · {/if}
								{#if item.delivery}Delivery · {/if}
								{#if item.supplies}Supplies · {/if}
								{#if item.onsite_support}Onsite support{/if}
								{#if !item.coffee_break && !item.setup && !item.clean_up && !item.delivery && !item.supplies && !item.onsite_support}No extras{/if}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeCateringItem(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No catering items added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!catering_data.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500"
				>{!catering_data.length ? 'Add at least one catering item' : ''}</span
			>
		</div>

		{#if errorMsg}
			<div class="text-sm text-red-600">{errorMsg}</div>
		{/if}

		<details class="rounded-xl border bg-gray-50 p-3">
			<summary class="cursor-pointer text-sm font-medium">Raw response</summary>
			<pre class="mt-2 overflow-auto text-xs">{JSON.stringify(res, null, 2)}</pre>
		</details>
	</section>
</div>