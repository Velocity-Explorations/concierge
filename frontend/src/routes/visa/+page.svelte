<script lang="ts">
    import { findVisaApiEstimatesVisaPost } from '../../client/sdk.gen';
    import type { VisaModel } from '../../client/types.gen';

    type VisaDataType = Array<VisaModel>;

    let visa_data = $state<VisaDataType>([]);

    let tempVisaData = $state<Partial<VisaModel>>({
        service_type: 'Travel', // or default from your enum
        from_date: '',
        to_date: '',
        from_country: '',
        to_country: ''
    });

    let res: unknown = $state();
    let loading = $state(false);
    let errorMsg = $state<string | null>(null);

    function addVisa() {
        if (!tempVisaData.service_type || !tempVisaData.from_date || !tempVisaData.to_date || !tempVisaData.from_country || !tempVisaData.to_country) return;

        const newVisa: VisaModel = {
            service_type: tempVisaData.service_type,
            from_date: tempVisaData.from_date,
            to_date: tempVisaData.to_date,
            from_country: tempVisaData.from_country,
            to_country: tempVisaData.to_country
        };

        visa_data = [...visa_data, newVisa];

        // Reset form
        tempVisaData = {
            service_type: tempVisaData.service_type,
            from_date: '',
            to_date: '',
            from_country: '',
            to_country: ''
        };
    }

    function removeVisa(idx: number) {
        visa_data = visa_data.filter((_, i) => i !== idx);
    }

    async function submit() {
        loading = true;
        errorMsg = null;
        try {
            res = await findVisaApiEstimatesVisaPost({
                body: { visa_data }
            });
        } catch (e: unknown) {
            errorMsg =
                (e instanceof Error ? e.message : String(e)) ?? 'Something went wrong fetching estimates.';
        } finally {
            loading = false;
        }
    }

    function getVisaSummary(visa: VisaModel): string {
        return `${visa.service_type} visa from ${visa.from_country} to ${visa.to_country} (${visa.from_date} to ${visa.to_date})`;
    }
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
    <header class="flex items-center justify-between">
        <h1 class="text-2xl font-semibold">Visa Estimates</h1>
        <div class="text-sm text-gray-500">Demo client</div>
    </header>

    <section class="space-y-4 rounded-2xl bg-white p-5 shadow">
        <h2 class="text-lg font-medium">Add visa request</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <label class="block text-sm font-medium"
                >Service Type
                <select class="mt-1 w-full rounded-xl border p-2" bind:value={tempVisaData.service_type}>
                    <option value="Travel">Travel</option>
                    <option value="Application">Application</option>
                    <option value="Delivery">Delivery</option>
                    <option value="Other">Other</option>
                    <!-- Add more types as needed -->
                </select>
            </label>
            <label class="block text-sm font-medium"
                >From Country
                <input class="mt-1 w-full rounded-xl border p-2" type="text" bind:value={tempVisaData.from_country} placeholder="e.g. USA" />
            </label>
            <label class="block text-sm font-medium"
                >To Country
                <input class="mt-1 w-full rounded-xl border p-2" type="text" bind:value={tempVisaData.to_country} placeholder="e.g. France" />
            </label>
            <label class="block text-sm font-medium"
                >From Date
                <input class="mt-1 w-full rounded-xl border p-2" type="date" bind:value={tempVisaData.from_date} />
            </label>
            <label class="block text-sm font-medium"
                >To Date
                <input class="mt-1 w-full rounded-xl border p-2" type="date" bind:value={tempVisaData.to_date} />
            </label>
        </div>

        <div class="flex gap-3 mt-4">
            <button
                type="button"
                class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
                onclick={addVisa}
                disabled={
                    !tempVisaData.service_type ||
                    !tempVisaData.from_date ||
                    !tempVisaData.to_date ||
                    !tempVisaData.from_country ||
                    !tempVisaData.to_country
                }
            >
                Add visa request
            </button>
            <button
                type="button"
                class="rounded-xl border px-4 py-2"
                onclick={() => (visa_data = [])}
                disabled={!visa_data.length}
            >
                Clear all
            </button>
        </div>

        {#if visa_data.length}
            <ul class="divide-y rounded-xl border">
                {#each visa_data as visa, i (i)}
                    <li class="flex items-center justify-between p-3">
                        <div class="flex-1 text-sm">
                            <div class="font-medium">
                                {getVisaSummary(visa)}
                            </div>
                        </div>
                        <button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeVisa(i)}
                            >Remove</button
                        >
                    </li>
                {/each}
            </ul>
        {:else}
            <p class="text-sm text-gray-500">No visa requests added yet.</p>
        {/if}
    </section>

    <section class="space-y-4 rounded-2xl bg-white p-5 shadow">
        <div class="flex items-center gap-3">
            <button
                class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
                onclick={submit}
                disabled={!visa_data.length || loading}
            >
                {#if loading}
                    <span class="animate-pulse">Fetching…</span>
                {:else}
                    Fetch estimates
                {/if}
            </button>
            <span class="text-sm text-gray-500"
                >{!visa_data.length ? 'Add at least one visa request' : ''}</span
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