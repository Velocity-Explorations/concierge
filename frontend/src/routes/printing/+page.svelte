<script lang="ts">
	import { findPrintingApiEstimatesPrintingPost } from '../../client/sdk.gen';
	import type { PrintingModel } from '../../client/types.gen';

	type PrintingDataType = Array<PrintingModel>;

	let printing_data = $state<PrintingDataType>([]);

	let tempPrintingData = $state<Partial<PrintingModel>>({
		location: 'New York, NY',
		bw_single_sided: 0,
		bw_double_sided: 0,
		color_single_sided: 0,
		color_double_sided: 0,
		certificate_card_stock: 0,
		simple_frame: 0,
		name_tag_cardstock_with_lanyard: 0,
		table_tent_cardstock: 0,
		binding_spiral_bound_with_dividers: 0,
		binding_3ring_binder_with_dividers: 0,
		delivery: false
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addPrinting() {
		if (!tempPrintingData.location) return;

		const newPrinting: PrintingModel = {
			location: tempPrintingData.location,
			bw_single_sided: tempPrintingData.bw_single_sided ?? 0,
			bw_double_sided: tempPrintingData.bw_double_sided ?? 0,
			color_single_sided: tempPrintingData.color_single_sided ?? 0,
			color_double_sided: tempPrintingData.color_double_sided ?? 0,
			certificate_card_stock: tempPrintingData.certificate_card_stock ?? 0,
			simple_frame: tempPrintingData.simple_frame ?? 0,
			name_tag_cardstock_with_lanyard: tempPrintingData.name_tag_cardstock_with_lanyard ?? 0,
			table_tent_cardstock: tempPrintingData.table_tent_cardstock ?? 0,
			binding_spiral_bound_with_dividers: tempPrintingData.binding_spiral_bound_with_dividers ?? 0,
			binding_3ring_binder_with_dividers: tempPrintingData.binding_3ring_binder_with_dividers ?? 0,
			delivery: tempPrintingData.delivery ?? false
		};

		printing_data = [...printing_data, newPrinting];

		// Reset form but keep location for convenience
		tempPrintingData = {
			location: tempPrintingData.location,
			bw_single_sided: 0,
			bw_double_sided: 0,
			color_single_sided: 0,
			color_double_sided: 0,
			certificate_card_stock: 0,
			simple_frame: 0,
			name_tag_cardstock_with_lanyard: 0,
			table_tent_cardstock: 0,
			binding_spiral_bound_with_dividers: 0,
			binding_3ring_binder_with_dividers: 0,
			delivery: false
		};
	}

	function removePrinting(idx: number) {
		printing_data = printing_data.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findPrintingApiEstimatesPrintingPost({
				body: { printing_data }
			});
		} catch (e: unknown) {
			errorMsg =
				(e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
		} finally {
			loading = false;
		}
	}

	function getPrintingSummary(printing: PrintingModel): string {
		const items = [];
		
		// Printing items
		if ((printing.bw_single_sided ?? 0) > 0) items.push(`${printing.bw_single_sided} B/W Single sided pages`);
		if ((printing.bw_double_sided ?? 0) > 0) items.push(`${printing.bw_double_sided} B/W Double sided pages`);
		if ((printing.color_single_sided ?? 0) > 0) items.push(`${printing.color_single_sided} Color Single sided pages`);
		if ((printing.color_double_sided ?? 0) > 0) items.push(`${printing.color_double_sided} Color Double sided pages`);
		
		// Production items
		if ((printing.certificate_card_stock ?? 0) > 0) items.push(`${printing.certificate_card_stock} Certificate/Card Stock`);
		if ((printing.simple_frame ?? 0) > 0) items.push(`${printing.simple_frame} Simple Frame(s)`);
		if ((printing.name_tag_cardstock_with_lanyard ?? 0) > 0) items.push(`${printing.name_tag_cardstock_with_lanyard} Name Tag(s) w/ Lanyard`);
		if ((printing.table_tent_cardstock ?? 0) > 0) items.push(`${printing.table_tent_cardstock} Table Tent(s)`);
		
		// Materials items
		if ((printing.binding_spiral_bound_with_dividers ?? 0) > 0) items.push(`${printing.binding_spiral_bound_with_dividers} Spiral Bound w/ Dividers`);
		if ((printing.binding_3ring_binder_with_dividers ?? 0) > 0) items.push(`${printing.binding_3ring_binder_with_dividers} 3-Ring Binder(s) w/ Dividers`);
		
		const services = [];
		if (printing.delivery) services.push('Delivery');
		
		return items.length > 0 ? items.join(', ') + (services.length > 0 ? ` + ${services.join(', ')}` : '') : 'No items selected';
	}
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Printing Estimates</h1>
		<div class="text-sm text-gray-500">Demo client</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add printing request</h2>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-1">
			<label class="block text-sm font-medium"
				>Location
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempPrintingData.location}
					placeholder="e.g. New York, NY"
				/>
			</label>
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Printing</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium"
					>B/W Single sided (pages)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.bw_single_sided}
					/>
				</label>
				<label class="block text-sm font-medium"
					>B/W Double sided (pages)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.bw_double_sided}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Color Single sided (pages)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.color_single_sided}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Color Double sided (pages)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.color_double_sided}
					/>
				</label>
			</div>
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Production</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium"
					>Certificate, Card Stock
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.certificate_card_stock}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Simple Frame
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.simple_frame}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Name Tag (Cardstock) w/ Lanyard
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.name_tag_cardstock_with_lanyard}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Table Tent (Cardstock)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.table_tent_cardstock}
					/>
				</label>
			</div>
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Materials - Other</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium"
					>Binding - Spiral bound w/ Dividers
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.binding_spiral_bound_with_dividers}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Binding - 3-Ring Binder w/ Dividers
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempPrintingData.binding_3ring_binder_with_dividers}
					/>
				</label>
			</div>
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Services</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempPrintingData.delivery}
						class="rounded"
					/>
					Delivery
				</label>
			</div>
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addPrinting}
				disabled={!tempPrintingData.location}
			>
				Add printing request
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (printing_data = [])}
				disabled={!printing_data.length}
			>
				Clear all
			</button>
		</div>

		{#if printing_data.length}
			<ul class="divide-y rounded-xl border">
				{#each printing_data as printing, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{printing.location}
							</div>
							<div class="mt-1 text-xs text-gray-500">
								{getPrintingSummary(printing)}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removePrinting(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No printing requests added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!printing_data.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500"
				>{!printing_data.length ? 'Add at least one printing request' : ''}</span
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