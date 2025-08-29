<script lang="ts">
    import { findGroundTransportApiEstimatesGroundTransportPost } from '../../client/sdk.gen';
    import type { GroundTransportModel } from '../../client/types.gen';

    type GroundTransportDataType = Array<GroundTransportModel>;

    let ground_transport_data = $state<GroundTransportDataType>([]);

    let tempGroundTransportData = $state<Partial<GroundTransportModel>>({
        country: 'USA',
        vehicle_type: 'Sedan',
        airport_arrival: false,
        airport_departure: false,
        outside_city_limits_rate: false,
        rate_type: 'Hourly'
    });

    let res: unknown = $state();
    let loading = $state(false);
    let errorMsg = $state<string | null>(null);

    function addGroundTransport() {
        if (!tempGroundTransportData.vehicle_type || !tempGroundTransportData.rate_type) return;

        const newTransport: GroundTransportModel = {
            country: tempGroundTransportData.country,
            vehicle_type: tempGroundTransportData.vehicle_type,
            airport_arrival: tempGroundTransportData.airport_arrival ?? false,
            airport_departure: tempGroundTransportData.airport_departure ?? false,
            outside_city_limits_rate: tempGroundTransportData.outside_city_limits_rate ?? false,
            rate_type: tempGroundTransportData.rate_type
        };

        ground_transport_data = [...ground_transport_data, newTransport];

        // Reset form
        tempGroundTransportData = {
            country: tempGroundTransportData.country,
            vehicle_type: tempGroundTransportData.vehicle_type,
            airport_arrival: false,
            airport_departure: false,
            outside_city_limits_rate: false,
            rate_type: tempGroundTransportData.rate_type
        };
    }

    function removeGroundTransport(idx: number) {
        ground_transport_data = ground_transport_data.filter((_, i) => i !== idx);
    }

    async function submit() {
        loading = true;
        errorMsg = null;
        try {
            res = await findGroundTransportApiEstimatesGroundTransportPost({
                body: { ground_transport_data }
            });
        } catch (e: unknown) {
            errorMsg =
                (e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
        } finally {
            loading = false;
        }
    }

    function getGroundTransportSummary(gt: GroundTransportModel): string {
        let summary = `${gt.vehicle_type} (${gt.rate_type})`;
        const details = [];
        if (gt.airport_arrival) details.push('Airport Arrival');
        if (gt.airport_departure) details.push('Airport Departure');
        if (gt.outside_city_limits_rate) details.push('Outside City Limits');
        return details.length ? `${summary} - ${details.join(', ')}` : summary;
    }
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
    <header class="flex items-center justify-between">
        <h1 class="text-2xl font-semibold">Ground Transport Estimates</h1>
        <div class="text-sm text-gray-500">Demo client</div>
    </header>

    <section class="space-y-4 rounded-2xl bg-white p-5 shadow">
        <h2 class="text-lg font-medium">Add ground transport request</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <label class="block text-sm font-medium"
                >Country
                <input class="mt-1 w-full rounded-xl border p-2" type="text" bind:value={tempGroundTransportData.country} placeholder="e.g. USA" />
            </label>
            <label class="block text-sm font-medium"
                >Vehicle Type
                <select class="mt-1 w-full rounded-xl border p-2" bind:value={tempGroundTransportData.vehicle_type}>
                    <option value="Sedan">Sedan</option>
                    <option value="SUV">SUV</option>
                    <option value="Van">Van</option>
                    <option value="Large Van">Large Van</option>
                    <option value="Bus">Bus</option>
                </select>
            </label>
            <label class="block text-sm font-medium"
                >Rate Type
                <select class="mt-1 w-full rounded-xl border p-2" bind:value={tempGroundTransportData.rate_type}>
                    <option value="Hourly">Hourly</option>
                    <option value="Half Day">Half Day</option>
                    <option value="Daily">Daily</option>
                </select>
            </label>
            <label class="flex items-center gap-2 text-sm font-medium"
                ><input type="checkbox" bind:checked={tempGroundTransportData.airport_arrival} /> Airport Arrival
            </label>
            <label class="flex items-center gap-2 text-sm font-medium"
                ><input type="checkbox" bind:checked={tempGroundTransportData.airport_departure} /> Airport Departure
            </label>
            <label class="flex items-center gap-2 text-sm font-medium"
                ><input type="checkbox" bind:checked={tempGroundTransportData.outside_city_limits_rate} /> Outside City Limits Rate
            </label>
        </div>

        <div class="flex gap-3 mt-4">
            <button
                type="button"
                class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
                onclick={addGroundTransport}
                disabled={
                    !tempGroundTransportData.vehicle_type ||
                    !tempGroundTransportData.rate_type
                }
            >
                Add ground transport request
            </button>
            <button
                type="button"
                class="rounded-xl border px-4 py-2"
                onclick={() => (ground_transport_data = [])}
                disabled={!ground_transport_data.length}
            >
                Clear all
            </button>
        </div>

        {#if ground_transport_data.length}
            <ul class="divide-y rounded-xl border">
                {#each ground_transport_data as gt, i (i)}
                    <li class="flex items-center justify-between p-3">
                        <div class="flex-1 text-sm">
                            <div class="font-medium">
                                {getGroundTransportSummary(gt)}
                            </div>
                        </div>
                        <button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeGroundTransport(i)}
                            >Remove</button
                        >
                    </li>
                {/each}
            </ul>
        {:else}
            <p class="text-sm text-gray-500">No ground transport requests added yet.</p>
        {/if}
    </section>

    <section class="space-y-4 rounded-2xl bg-white p-5 shadow">
        <div class="flex items-center gap-3">
            <button
                class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
                onclick={submit}
                disabled={!ground_transport_data.length || loading}
            >
                {#if loading}
                    <span class="animate-pulse">Fetching…</span>
                {:else}
                    Fetch estimates
                {/if}
            </button>
            <span class="text-sm text-gray-500"
                >{!ground_transport_data.length ? 'Add at least one ground transport request' : ''}</span
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