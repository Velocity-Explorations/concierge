<script lang="ts">
	import { findEquipmentApiEstimatesEquipmentPost } from '../../client/sdk.gen';
	import type { EquipmentModel } from '../../client/types.gen';

	type EquipmentDataType = Array<EquipmentModel>;

	let equipment_data = $state<EquipmentDataType>([]);

	let tempEquipmentData = $state<Partial<EquipmentModel>>({
		location: 'New York, NY',
		duration_days: 1,
		laptop: 0,
		portable_printer: 0,
		large_printer: 0,
		projector: 0,
		equipment_other: 0,
		cell_phone: 0,
		cell_phone_minutes: 0,
		hot_spot: 0,
		satellite_phone: 0,
		locator_beacon: 0,
		setup_and_cleanup: false,
		onsite_support_equipment: false,
		equipment_other_description: ''
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addEquipment() {
		if (!tempEquipmentData.location || !tempEquipmentData.duration_days) return;

		const newEquipment: EquipmentModel = {
			location: tempEquipmentData.location,
			duration_days: tempEquipmentData.duration_days,
			laptop: tempEquipmentData.laptop ?? 0,
			portable_printer: tempEquipmentData.portable_printer ?? 0,
			large_printer: tempEquipmentData.large_printer ?? 0,
			projector: tempEquipmentData.projector ?? 0,
			equipment_other: tempEquipmentData.equipment_other ?? 0,
			cell_phone: tempEquipmentData.cell_phone ?? 0,
			cell_phone_minutes: tempEquipmentData.cell_phone_minutes ?? 0,
			hot_spot: tempEquipmentData.hot_spot ?? 0,
			satellite_phone: tempEquipmentData.satellite_phone ?? 0,
			locator_beacon: tempEquipmentData.locator_beacon ?? 0,
			setup_and_cleanup: tempEquipmentData.setup_and_cleanup ?? false,
			onsite_support_equipment: tempEquipmentData.onsite_support_equipment ?? false,
			equipment_other_description: tempEquipmentData.equipment_other_description ?? ''
		};

		equipment_data = [...equipment_data, newEquipment];

		// Reset form but keep location and duration for convenience
		tempEquipmentData = {
			location: tempEquipmentData.location,
			duration_days: tempEquipmentData.duration_days,
			laptop: 0,
			portable_printer: 0,
			large_printer: 0,
			projector: 0,
			equipment_other: 0,
			cell_phone: 0,
			cell_phone_minutes: 0,
			hot_spot: 0,
			satellite_phone: 0,
			locator_beacon: 0,
			setup_and_cleanup: false,
			onsite_support_equipment: false,
			equipment_other_description: ''
		};
	}

	function removeEquipment(idx: number) {
		equipment_data = equipment_data.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findEquipmentApiEstimatesEquipmentPost({
				body: { equipment_data }
			});
		} catch (e: unknown) {
			errorMsg =
				(e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
		} finally {
			loading = false;
		}
	}

	function getEquipmentSummary(equipment: EquipmentModel): string {
		const items = [];
		if ((equipment.laptop ?? 0) > 0) items.push(`${equipment.laptop} Laptop(s)`);
		if ((equipment.portable_printer ?? 0) > 0) items.push(`${equipment.portable_printer} Portable Printer(s)`);
		if ((equipment.large_printer ?? 0) > 0) items.push(`${equipment.large_printer} Large Printer(s)`);
		if ((equipment.projector ?? 0) > 0) items.push(`${equipment.projector} Projector(s)`);
		if ((equipment.equipment_other ?? 0) > 0) items.push(`${equipment.equipment_other} Other Equipment`);
		if ((equipment.cell_phone ?? 0) > 0) items.push(`${equipment.cell_phone} Cell Phone(s)`);
		if ((equipment.cell_phone_minutes ?? 0) > 0) items.push(`${equipment.cell_phone_minutes} Cell Phone Minutes`);
		if ((equipment.hot_spot ?? 0) > 0) items.push(`${equipment.hot_spot} Hot Spot(s)`);
		if ((equipment.satellite_phone ?? 0) > 0) items.push(`${equipment.satellite_phone} Satellite Phone(s)`);
		if ((equipment.locator_beacon ?? 0) > 0) items.push(`${equipment.locator_beacon} Locator Beacon(s)`);
		
		const services = [];
		if (equipment.setup_and_cleanup) services.push('Setup & Cleanup');
		if (equipment.onsite_support_equipment) services.push('Onsite Support');
		
		return items.length > 0 ? items.join(', ') + (services.length > 0 ? ` + ${services.join(', ')}` : '') : 'No equipment selected';
	}
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Equipment Estimates</h1>
		<div class="text-sm text-gray-500">Demo client</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add equipment request</h2>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			<label class="block text-sm font-medium"
				>Location
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempEquipmentData.location}
					placeholder="e.g. New York, NY"
				/>
			</label>
			<label class="block text-sm font-medium"
				>Duration (days)
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="1"
					bind:value={tempEquipmentData.duration_days}
				/>
			</label>
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Equipment Quantities</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
				<label class="block text-sm font-medium"
					>Laptops
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.laptop}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Portable Printers
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.portable_printer}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Large Printers
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.large_printer}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Projectors
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.projector}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Equipment - Other
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.equipment_other}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Cell Phones
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.cell_phone}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Cell Phone Minutes
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.cell_phone_minutes}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Hot Spots
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.hot_spot}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Satellite Phones
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.satellite_phone}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Locator Beacons
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempEquipmentData.locator_beacon}
					/>
				</label>
			</div>

			{#if tempEquipmentData.equipment_other && tempEquipmentData.equipment_other > 0}
				<label class="block text-sm font-medium"
					>Other Equipment Description
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="text"
						bind:value={tempEquipmentData.equipment_other_description}
						placeholder="Describe the other equipment needed"
					/>
				</label>
			{/if}
		</div>

		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Services</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempEquipmentData.setup_and_cleanup}
						class="rounded"
					/>
					Setup and Cleanup
				</label>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempEquipmentData.onsite_support_equipment}
						class="rounded"
					/>
					Onsite Support - Equipment
				</label>
			</div>
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addEquipment}
				disabled={!tempEquipmentData.location || !tempEquipmentData.duration_days}
			>
				Add equipment request
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (equipment_data = [])}
				disabled={!equipment_data.length}
			>
				Clear all
			</button>
		</div>

		{#if equipment_data.length}
			<ul class="divide-y rounded-xl border">
				{#each equipment_data as equipment, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{equipment.location}
							</div>
							<div class="text-gray-500">{equipment.duration_days} day(s)</div>
							<div class="mt-1 text-xs text-gray-500">
								{getEquipmentSummary(equipment)}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeEquipment(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No equipment requests added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!equipment_data.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500"
				>{!equipment_data.length ? 'Add at least one equipment request' : ''}</span
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