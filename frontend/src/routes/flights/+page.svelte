<script lang="ts">
	import { findEstimatesApiEstimatesFlightsPost } from '../../client/sdk.gen';
	import type { OneWayFlight, RoundTripFlight, PassengerModel } from '../../client/types.gen';

	type FetchModeType = OneWayFlight['fetch_mode'];
	type FlightType = OneWayFlight | RoundTripFlight;
	type PassengerType = PassengerModel;
	type SeatType = OneWayFlight['seat'];
	type TripKind = 'one-way' | 'round-trip';

	const FETCH_MODES: FetchModeType[] = ['common', 'fallback', 'force-fallback', 'local'];
	const SEAT_TYPES: SeatType[] = ['economy', 'premium-economy', 'business', 'first'];
	const TRIP_KINDS: TripKind[] = ['one-way', 'round-trip'];

	let fetch_mode: FetchModeType = $state('common');
	let flights = $state<FlightType[]>([]);
	const passengers = $state<PassengerType>({ adults: 1 });
	let seat = $state<SeatType>('economy');
	let trip_kind = $state<TripKind>('round-trip');


	let tempFlightData = $state({
		outbound_date: new Date().toISOString().split('T')[0],
		return_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
		from_country: 'United States',
		to_country: 'United States',
		from_city: "New York",
		to_city: "San Francisco",
		max_stops: 0,
		max_combinations: 20
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	function addFlight() {
		if (!tempFlightData.from_country || !tempFlightData.to_country || !tempFlightData.from_city || !tempFlightData.to_city) return;
		if (trip_kind === 'one-way' && !tempFlightData.outbound_date) return;
		if (
			trip_kind === 'round-trip' &&
			(!tempFlightData.outbound_date || !tempFlightData.return_date)
		)
			return;

		let newFlight: FlightType;


		if (trip_kind === 'one-way') {
			newFlight = {
				kind: 'one-way',
				date: tempFlightData.outbound_date,
				from_country: tempFlightData.from_country,
				to_country: tempFlightData.to_country,
				from_city: tempFlightData.from_city,
				to_city: tempFlightData.to_city,
				max_stops: tempFlightData.max_stops || undefined,
				seat,
				passengers: { ...passengers },
				fetch_mode
			} as OneWayFlight;
		} else {
			newFlight = {
				kind: 'round-trip',
				outbound_date: tempFlightData.outbound_date,
				return_date: tempFlightData.return_date,
				from_country: tempFlightData.from_country,
				to_country: tempFlightData.to_country,
				from_city: tempFlightData.from_city,
				to_city: tempFlightData.to_city,
				max_stops: tempFlightData.max_stops || undefined,
				seat,
				passengers: { ...passengers },
				fetch_mode,
				max_combinations: tempFlightData.max_combinations
			} as RoundTripFlight;
		}

		flights = [...flights, newFlight];

		// Reset form
		tempFlightData = {
			outbound_date: tempFlightData.outbound_date,
			return_date: tempFlightData.return_date,
			from_country: tempFlightData.from_country,
			to_country: tempFlightData.to_country,
			from_city: tempFlightData.from_city,
			to_city: tempFlightData.to_city,
			max_stops: 0,
			max_combinations: 20

		};
	}

	function removeFlight(idx: number) {
		flights = flights.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findEstimatesApiEstimatesFlightsPost({
				body: { flights }
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
				>From Country
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"

					bind:value={tempFlightData.from_country}
					oninput={(e) =>
						(tempFlightData.from_country = (e.target as HTMLInputElement).value)}
					placeholder="e.g. United States"
				/>
			</label>
			<label class="block text-sm font-medium"
				>To Country
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempFlightData.to_country}
					oninput={(e) =>
						(tempFlightData.to_country = (e.target as HTMLInputElement).value)}
					placeholder="e.g. Canada"
				/>
			</label>
			<label class="block text-sm font-medium"
				>From City
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempFlightData.from_city}
					oninput={(e) =>
						(tempFlightData.from_city = (e.target as HTMLInputElement).value)}
					placeholder="e.g. New York"
				/>
			</label>
			<label class="block text-sm font-medium"
				>To City
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="text"
					bind:value={tempFlightData.to_city}
					oninput={(e) =>
						(tempFlightData.to_city = (e.target as HTMLInputElement).value)}
					placeholder="e.g. Ottawa"

				/>
			</label>
			<label class="block text-sm font-medium"
				>Departure Date
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="date"
					bind:value={tempFlightData.outbound_date}
				/>
			</label>
			{#if trip_kind === 'round-trip'}
				<label class="block text-sm font-medium"
					>Return Date
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="date"
						bind:value={tempFlightData.return_date}
					/>
				</label>
			{/if}
			<label class="block text-sm font-medium"
				>Max stops
				<input
					class="mt-1 w-full rounded-xl border p-2"
					type="number"
					min="0"
					bind:value={tempFlightData.max_stops}
				/>
			</label>
			{#if trip_kind === 'round-trip'}
				<label class="block text-sm font-medium"
					>Max combinations
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="1"
						max="100"
						bind:value={tempFlightData.max_combinations}
					/>
				</label>
			{/if}
		</div>
		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addFlight}
			>
				Add flight
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (flights = [])}
				disabled={!flights.length}
			>
				Clear all
			</button>
		</div>

		{#if flights.length}
			<ul class="divide-y rounded-xl border">
				{#each flights as flight, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="flex-1 text-sm">
							<div class="font-medium">
								{flight.from_city.toUpperCase()} → {flight.to_city.toUpperCase()}
							</div>
							<div class="text-gray-500">{flight.kind === 'one-way' ? (flight as OneWayFlight).date : `${(flight as RoundTripFlight).outbound_date} - ${(flight as RoundTripFlight).return_date}`} · max {flight.max_stops} stop(s)</div>
							<div class="mt-1 text-xs text-gray-500">
								{flight.seat} · {flight.kind} · {flight.passengers.adults} adult(s) · {flight.fetch_mode}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeFlight(i)}
							>Remove</button
						>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No flights added yet.</p>
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
					bind:value={passengers.adults}
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
				{#each TRIP_KINDS as item (item)}
					<label class="inline-flex items-center gap-2">
						<input class="sr-only" type="radio" bind:group={trip_kind} value={item} />
						<span
							class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
							class:!bg-black={trip_kind === item}
							class:!text-white={trip_kind === item}
							class:!border-black={trip_kind === item}>{item}</span
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
				disabled={!flights.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Fetch estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500">{!flights.length ? 'Add at least one flight' : ''}</span>
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
