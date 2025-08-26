<script lang="ts">
	import { findEstimatesApiEstimatesFlightsPost } from '../../client/sdk.gen';
	import type { FlightDataModel, PassengerModel } from '../../client/types.gen';

	type FetchModeType = FlightDataModel['fetch_mode'];
	type FlightDataType = Array<FlightDataModel>;
	type PassengerType = PassengerModel;
	type SeatType = FlightDataModel['seat'];
	type TripType = FlightDataModel['trip'];

	const FETCH_MODES: FetchModeType[] = ['common', 'fallback', 'force-fallback', 'local'];
	const SEAT_TYPES: SeatType[] = ['economy', 'premium-economy', 'business', 'first'];
	const TRIP_TYPES: TripType[] = ['round-trip', 'one-way', 'multi-city'];

	let fetch_mode: FetchModeType = $state('common');
	let flight_data = $state<FlightDataType>([]);
	const passenger = $state<PassengerType>({ adults: 1 });
	let seat = $state<SeatType>('economy');
	let trip = $state<TripType>('round-trip');

	let tempFlightdata = $state<Partial<FlightDataModel>>({
		date: new Date().toISOString().split('T')[0],
		from_airport: 'MCO',
		to_airport: 'JFK',
		max_stops: 0
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addSegment() {
		if (!tempFlightdata.from_airport || !tempFlightdata.to_airport || !tempFlightdata.date) return;

		const newSegment: FlightDataModel = {
			date: tempFlightdata.date,
			from_airport: tempFlightdata.from_airport,
			to_airport: tempFlightdata.to_airport,
			max_stops: tempFlightdata.max_stops ?? 0,
			trip,
			seat,
			passenger: { ...passenger },
			fetch_mode
		};

		flight_data = [...flight_data, newSegment];

		// reset destination to encourage round-trip defaults
		tempFlightdata = {
			date: tempFlightdata.date,
			from_airport: tempFlightdata.to_airport,
			to_airport: tempFlightdata.from_airport,
			max_stops: 0
		};
	}

	function removeSegment(idx: number) {
		flight_data = flight_data.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findEstimatesApiEstimatesFlightsPost({
				body: { flight_data }
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
		<h1 class="text-2xl font-semibold">Flight Estimates</h1>
		<div class="text-sm text-gray-500">Demo client</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add flight segment</h2>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			<label class="block text-sm font-medium"
				>From airport
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempFlightdata.from_airport}
					oninput={(e) =>
						(tempFlightdata.from_airport = (e.target as HTMLInputElement).value.toUpperCase())}
					placeholder="e.g. SFO"
				/>
			</label>
			<label class="block text-sm font-medium"
				>To airport
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempFlightdata.to_airport}
					oninput={(e) =>
						(tempFlightdata.to_airport = (e.target as HTMLInputElement).value.toUpperCase())}
					placeholder="e.g. JFK"
				/>
			</label>
			<label class="block text-sm font-medium"
				>Date
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="date"
					bind:value={tempFlightdata.date}
				/>
			</label>
			<label class="block text-sm font-medium"
				>Max stops
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="0"
					bind:value={tempFlightdata.max_stops}
				/>
			</label>
		</div>
		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addSegment}
			>
				Add segment
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (flight_data = [])}
				disabled={!flight_data.length}
			>
				Clear all
			</button>
		</div>

		{#if flight_data.length}
			<ul class="divide-y rounded-xl border">
				{#each flight_data as flight, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{flight.from_airport.toUpperCase()} → {flight.to_airport.toUpperCase()}
							</div>
							<div class="text-gray-500">{flight.date} · max {flight.max_stops} stop(s)</div>
							<div class="mt-1 text-xs text-gray-500">
								{flight.seat} · {flight.trip} · {flight.passenger.adults} adult(s) · {flight.fetch_mode}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeSegment(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No segments added yet.</p>
		{/if}
	</section>

	<section class="grid grid-cols-1 gap-6 md:grid-cols-3">
		<div class="space-y-3 rounded-2xl bg-white p-5 shadow">
			<h3 class="font-medium">Passengers</h3>
			<label class="block text-sm"
				>Adults
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="1"
					bind:value={passenger.adults}
				/>
			</label>
		</div>

		<div class="space-y-3 rounded-2xl bg-white p-5 shadow">
			<h3 class="font-medium">Fetch mode</h3>
			<div class="flex flex-wrap gap-2">
				{#each FETCH_MODES as item (item)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={fetch_mode} value={item} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={fetch_mode === item}
							class:!text-white={fetch_mode === item}
							class:!border-black={fetch_mode === item}>{item}</span
						>
					</label>
				{/each}
			</div>
		</div>

		<div class="space-y-3 rounded-2xl bg-white p-5 shadow">
			<h3 class="font-medium">Seat</h3>
			<div class="flex flex-wrap gap-2">
				{#each SEAT_TYPES as item (item)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={seat} value={item} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={seat === item}
							class:!text-white={seat === item}
							class:!border-black={seat === item}>{item}</span
						>
					</label>
				{/each}
			</div>
		</div>

		<div class="space-y-3 rounded-2xl bg-white p-5 shadow md:col-span-3">
			<h3 class="font-medium">Trip type</h3>
			<div class="flex flex-wrap gap-2">
				{#each TRIP_TYPES as item (item)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={trip} value={item} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={trip === item}
							class:!text-white={trip === item}
							class:!border-black={trip === item}>{item}</span
						>
					</label>
				{/each}
			</div>
		</div>
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!flight_data.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500"
				>{!flight_data.length ? 'Add at least one segment' : ''}</span
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
