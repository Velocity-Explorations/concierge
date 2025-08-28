<script lang="ts">
	import { findVenueApiEstimatesVenuePost } from '../../client/sdk.gen';
	import type { VenueModel, BreakoutRoomModel, CoffeeBreakModel, AVPackageModel, AVEquipmentModel, MiscModel } from '../../client/types.gen';

	type VenueDataType = Array<VenueModel>;

	let venue_data = $state<VenueDataType>([]);

	type VenueType = VenueModel['venue_type'];
	const VENUE_TYPES: { value: VenueType; label: string; description: string }[] = [
		{ value: 'venue_package', label: 'Venue Package', description: 'room, water, A/V, catering' },
		{ value: 'conference_room_package', label: 'Conference Room Package', description: 'room, water, A/V, coffee breaks' },
		{ value: 'conference_room', label: 'Conference Room', description: 'bottled water and pen/notepad only' }
	];

	let tempVenueData = $state<{
		location: string;
		duration_hours: number;
		pax: number;
		venue_type: VenueType;
		breakout_room: BreakoutRoomModel;
		coffee_breaks: CoffeeBreakModel;
		av_package: AVPackageModel;
		av_equipment: AVEquipmentModel;
		misc: MiscModel;
	}>({
		location: 'New York, NY',
		duration_hours: 8,
		pax: 20,
		venue_type: 'venue_package',
		breakout_room: {
			quantity: 0,
			setup: false
		},
		coffee_breaks: {
			am_break_per_person: 0,
			pm_break_per_person: 0,
			coffee_tea_station_all_day_per_person: 0
		},
		av_package: {
			quantity: 0,
			includes_description: ''
		},
		av_equipment: {
			projector: 0,
			sound_system: 0,
			screen: 0,
			tabletop_microphone: 0,
			laptop: 0,
			power_strip_extension_cords: 0,
			printer: 0
		},
		misc: {
			setup_cleanup: false,
			onsite_support: false,
			delivery: false,
			meeting_supplies: false,
			other: false,
			other_description: ''
		}
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addVenue() {
		if (!tempVenueData.location || !tempVenueData.duration_hours || !tempVenueData.pax) return;

		const newVenue: VenueModel = {
			location: tempVenueData.location,
			duration_hours: tempVenueData.duration_hours,
			pax: tempVenueData.pax,
			venue_type: tempVenueData.venue_type,
			breakout_room: { ...tempVenueData.breakout_room },
			coffee_breaks: { ...tempVenueData.coffee_breaks },
			av_package: { ...tempVenueData.av_package },
			av_equipment: { ...tempVenueData.av_equipment },
			misc: { ...tempVenueData.misc }
		};

		venue_data = [...venue_data, newVenue];

		// Reset form but keep location, duration, and pax for convenience
		tempVenueData = {
			location: tempVenueData.location,
			duration_hours: tempVenueData.duration_hours,
			pax: tempVenueData.pax,
			venue_type: 'venue_package',
			breakout_room: {
				quantity: 0,
				setup: false
			},
			coffee_breaks: {
				am_break_per_person: 0,
				pm_break_per_person: 0,
				coffee_tea_station_all_day_per_person: 0
			},
			av_package: {
				quantity: 0,
				includes_description: ''
			},
			av_equipment: {
				projector: 0,
				sound_system: 0,
				screen: 0,
				tabletop_microphone: 0,
				laptop: 0,
				power_strip_extension_cords: 0,
				printer: 0
			},
			misc: {
				setup_cleanup: false,
				onsite_support: false,
				delivery: false,
				meeting_supplies: false,
				other: false,
				other_description: ''
			}
		};
	}

	function removeVenue(idx: number) {
		venue_data = venue_data.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findVenueApiEstimatesVenuePost({
				body: { venue_data }
			});
		} catch (e: unknown) {
			errorMsg =
				(e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
		} finally {
			loading = false;
		}
	}

	function getVenueSummary(venue: VenueModel): string {
		const items = [];
		
		// Venue type
		const venueTypeLabel = VENUE_TYPES.find(t => t.value === venue.venue_type)?.label || venue.venue_type;
		items.push(venueTypeLabel);
		
		// Breakout room
		if ((venue.breakout_room.quantity ?? 0) > 0) {
			const setupText = venue.breakout_room.setup ? ' with setup' : '';
			items.push(`${venue.breakout_room.quantity} Breakout Room${setupText}`);
		}
		
		// Coffee services
		if ((venue.coffee_breaks.am_break_per_person ?? 0) > 0) items.push(`${venue.coffee_breaks.am_break_per_person} AM Breaks`);
		if ((venue.coffee_breaks.pm_break_per_person ?? 0) > 0) items.push(`${venue.coffee_breaks.pm_break_per_person} PM Breaks`);
		if ((venue.coffee_breaks.coffee_tea_station_all_day_per_person ?? 0) > 0) items.push(`${venue.coffee_breaks.coffee_tea_station_all_day_per_person} All-Day Coffee/Tea`);
		
		// A/V
		if ((venue.av_package.quantity ?? 0) > 0) items.push(`${venue.av_package.quantity} A/V Package`);
		if ((venue.av_equipment.projector ?? 0) > 0) items.push(`${venue.av_equipment.projector} Projector(s)`);
		if ((venue.av_equipment.sound_system ?? 0) > 0) items.push(`${venue.av_equipment.sound_system} Sound System(s)`);
		if ((venue.av_equipment.screen ?? 0) > 0) items.push(`${venue.av_equipment.screen} Screen(s)`);
		if ((venue.av_equipment.tabletop_microphone ?? 0) > 0) items.push(`${venue.av_equipment.tabletop_microphone} Microphone(s)`);
		if ((venue.av_equipment.laptop ?? 0) > 0) items.push(`${venue.av_equipment.laptop} Laptop(s)`);
		if ((venue.av_equipment.power_strip_extension_cords ?? 0) > 0) items.push(`${venue.av_equipment.power_strip_extension_cords} Power Strip(s)`);
		if ((venue.av_equipment.printer ?? 0) > 0) items.push(`${venue.av_equipment.printer} Printer(s)`);
		
		const services = [];
		if (venue.misc.setup_cleanup) services.push('Setup/Cleanup');
		if (venue.misc.onsite_support) services.push('Onsite Support');
		if (venue.misc.delivery) services.push('Delivery');
		if (venue.misc.meeting_supplies) services.push('Meeting Supplies');
		if (venue.misc.other && venue.misc.other_description) services.push(`Other: ${venue.misc.other_description}`);
		
		return items.length > 0 ? items.join(', ') + (services.length > 0 ? ` + ${services.join(', ')}` : '') : 'No items selected';
	}
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Venue Estimates</h1>
		<div class="text-sm text-gray-500">Demo client</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add venue request</h2>
		
		<!-- Basic Info -->
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
			<label class="block text-sm font-medium"
				>Location
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempVenueData.location}
					placeholder="e.g. New York, NY"
				/>
			</label>
			<label class="block text-sm font-medium"
				>Duration (hours)
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="1"
					bind:value={tempVenueData.duration_hours}
				/>
			</label>
			<label class="block text-sm font-medium"
				>PAX (people)
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="1"
					bind:value={tempVenueData.pax}
				/>
			</label>
		</div>

		<!-- Venue Type Selection -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Venue Type</h3>
			<div class="flex flex-wrap gap-2">
				{#each VENUE_TYPES as venueType (venueType.value)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={tempVenueData.venue_type} value={venueType.value} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={tempVenueData.venue_type === venueType.value}
							class:!text-white={tempVenueData.venue_type === venueType.value}
							class:!border-black={tempVenueData.venue_type === venueType.value}
						>
							{venueType.label}
						</span>
					</label>
				{/each}
			</div>
			<p class="text-xs text-gray-500">
				{VENUE_TYPES.find(t => t.value === tempVenueData.venue_type)?.description}
			</p>
		</div>

		<!-- Breakout Room -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Breakout Room</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium"
					>Quantity
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.breakout_room.quantity}
					/>
				</label>
				<label class="flex items-center gap-2 text-sm font-medium mt-6">
					<input
						type="checkbox"
						bind:checked={tempVenueData.breakout_room.setup}
						class="rounded"
					/>
					Setup
				</label>
			</div>
		</div>

		<!-- Coffee Services -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Coffee Services</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
				<label class="block text-sm font-medium"
					>AM Break (per person)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.coffee_breaks.am_break_per_person}
					/>
				</label>
				<label class="block text-sm font-medium"
					>PM Break (per person)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.coffee_breaks.pm_break_per_person}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Coffee & Tea Station All Day (per person)
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.coffee_breaks.coffee_tea_station_all_day_per_person}
					/>
				</label>
			</div>
		</div>

		<!-- A/V Package -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">A/V Package</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium"
					>Package Quantity
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_package.quantity}
					/>
				</label>
				{#if (tempVenueData.av_package.quantity ?? 0) > 0}
					<label class="block text-sm font-medium"
						>Package Includes
						<input
							class="mt-1 w-full rounded-xl border p-2"
							type="text"
							bind:value={tempVenueData.av_package.includes_description}
							placeholder="Describe what the A/V package includes"
						/>
					</label>
				{/if}
			</div>
		</div>

		<!-- A/V Equipment -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">A/V Equipment</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
				<label class="block text-sm font-medium"
					>Projector
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.projector}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Sound System
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.sound_system}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Screen
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.screen}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Tabletop Microphone
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.tabletop_microphone}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Laptop
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.laptop}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Power Strip/Extension Cords
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.power_strip_extension_cords}
					/>
				</label>
				<label class="block text-sm font-medium"
					>Printer
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="0"
						bind:value={tempVenueData.av_equipment.printer}
					/>
				</label>
			</div>
		</div>

		<!-- Misc Services -->
		<div class="space-y-4">
			<h3 class="font-medium text-gray-900">Miscellaneous Services</h3>
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempVenueData.misc.setup_cleanup}
						class="rounded"
					/>
					Setup/Cleanup
				</label>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempVenueData.misc.onsite_support}
						class="rounded"
					/>
					Onsite Support
				</label>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempVenueData.misc.delivery}
						class="rounded"
					/>
					Delivery
				</label>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempVenueData.misc.meeting_supplies}
						class="rounded"
					/>
					Meeting Supplies
				</label>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input
						type="checkbox"
						bind:checked={tempVenueData.misc.other}
						class="rounded"
					/>
					Other
				</label>
			</div>
			{#if tempVenueData.misc.other}
				<label class="block text-sm font-medium"
					>Other Description
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="text"
						bind:value={tempVenueData.misc.other_description}
						placeholder="Describe the other services needed"
					/>
				</label>
			{/if}
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addVenue}
				disabled={!tempVenueData.location || !tempVenueData.duration_hours || !tempVenueData.pax}
			>
				Add venue request
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (venue_data = [])}
				disabled={!venue_data.length}
			>
				Clear all
			</button>
		</div>

		{#if venue_data.length}
			<ul class="divide-y rounded-xl border">
				{#each venue_data as venue, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{venue.location} - {venue.duration_hours} hours - {venue.pax} PAX
							</div>
							<div class="mt-1 text-xs text-gray-500">
								{getVenueSummary(venue)}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeVenue(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No venue requests added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!venue_data.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500"
				>{!venue_data.length ? 'Add at least one venue request' : ''}</span
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