<script lang="ts">
	import { findMealAndLodgingApiEstimatesPerDiemPost } from '../../client/sdk.gen';
	import type { CountryName, StayModel, UsStateCode } from '../../client/types.gen';


	type StayModelType = StayModel;

	let stays = $state<StayModelType[]>([]);

	let tempStay = $state<{
		days: number;
		location: {
			kind: 'us' | 'foreign';
			country: CountryName;
			state?: UsStateCode;
			city: string;
		};
		is_first_travel_day: boolean;
		is_last_travel_day: boolean;
		deduct_meals: boolean;
	}>({
		days: 1,
		location: {
			kind: 'us',
			country: 'UNITED_STATES',
			state: 'CA',
			city: 'San Francisco'
		},
		is_first_travel_day: false,
		is_last_travel_day: false,
		deduct_meals: false
	});

	// Handle switching between US and foreign location types
	$effect(() => {
		if (tempStay.location.kind === 'us') {
			tempStay.location.country = 'UNITED_STATES';
			if (!tempStay.location.state) {
				tempStay.location.state = 'CA';
			}
		} else if (tempStay.location.kind === 'foreign') {
			tempStay.location.country = ALL_COUNTRIES[0];
			tempStay.location.state = undefined;
		}
	});

	let res: any = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	const US_STATES: UsStateCode[] = [
		'AL',
		'AK',
		'AZ',
		'AR',
		'CA',
		'CO',
		'CT',
		'DE',
		'FL',
		'GA',
		'HI',
		'ID',
		'IL',
		'IN',
		'IA',
		'KS',
		'KY',
		'LA',
		'ME',
		'MD',
		'MA',
		'MI',
		'MN',
		'MS',
		'MO',
		'MT',
		'NE',
		'NV',
		'NH',
		'NJ',
		'NM',
		'NY',
		'NC',
		'ND',
		'OH',
		'OK',
		'OR',
		'PA',
		'RI',
		'SC',
		'SD',
		'TN',
		'TX',
		'UT',
		'VT',
		'VA',
		'WA',
		'WV',
		'WI',
		'WY',
		'DC'
	];

	const ALL_COUNTRIES: CountryName[] = [
		'AFGHANISTAN',
		'ALBANIA',
		'ALGERIA',
		'ANDORRA',
		'ANGOLA',
		'ANGUILLA',
		'ANTARCTICA',
		'ANTIGUA_AND_BARBUDA',
		'ARGENTINA',
		'ARMENIA',
		'ARUBA',
		'ASCENSION_ISLAND',
		'AUSTRALIA',
		'AUSTRIA',
		'AZERBAIJAN',
		'BAHAMAS_THE',
		'BAHRAIN',
		'BANGLADESH',
		'BARBADOS',
		'BELARUS',
		'BELGIUM',
		'BELIZE',
		'BENIN',
		'BERMUDA',
		'BHUTAN',
		'BOLIVIA',
		'BONAIRE_SINT_EUSTATIUS_SABA',
		'BOSNIA_AND_HERZEGOVINA',
		'BOTSWANA',
		'BRAZIL',
		'BRUNEI',
		'BULGARIA',
		'BURKINA_FASO',
		'BURMA',
		'BURUNDI',
		'CABO_VERDE',
		'CAMBODIA',
		'CAMEROON',
		'CANADA',
		'CAYMAN_ISLANDS',
		'CENTRAL_AFRICAN_REPUBLIC',
		'CHAD',
		'CHAGOS_ARCHIPELAGO',
		'CHILE',
		'CHINA',
		'COCOS_KEELING_ISLANDS',
		'COLOMBIA',
		'COMOROS',
		'COOK_ISLANDS',
		'COSTA_RICA',
		'COTE_DIVOIRE',
		'CROATIA',
		'CUBA',
		'CURACAO',
		'CYPRUS',
		'CZECHIA',
		'DPRK_NORTH_KOREA',
		'DRC_CONGO',
		'DENMARK',
		'DJIBOUTI',
		'DOMINICA',
		'DOMINICAN_REPUBLIC',
		'ECUADOR',
		'EGYPT',
		'EL_SALVADOR',
		'EQUATORIAL_GUINEA',
		'ERITREA',
		'ESTONIA',
		'ESWATINI',
		'ETHIOPIA',
		'FALKLAND_ISLANDS',
		'FAROE_ISLANDS',
		'FIJI',
		'FINLAND',
		'FRANCE',
		'FRENCH_GUIANA',
		'FRENCH_POLYNESIA',
		'GABON',
		'GAMBIA_THE',
		'GEORGIA',
		'GERMANY',
		'GHANA',
		'GIBRALTAR',
		'GREECE',
		'GREENLAND',
		'GRENADA',
		'GUADELOUPE',
		'GUATEMALA',
		'GUINEA',
		'GUINEA_BISSAU',
		'GUYANA',
		'HAITI',
		'HOLY_SEE',
		'HONDURAS',
		'HONG_KONG',
		'HUNGARY',
		'ICELAND',
		'INDIA',
		'INDONESIA',
		'IRAN',
		'IRAQ',
		'IRELAND',
		'ISRAEL',
		'ITALY',
		'JAMAICA',
		'JAPAN',
		'JORDAN',
		'KAZAKHSTAN',
		'KENYA',
		'KIRIBATI',
		'KOREA_SOUTH',
		'KOSOVO',
		'KUWAIT',
		'KYRGYZSTAN',
		'LAOS',
		'LATVIA',
		'LEBANON',
		'LESOTHO',
		'LIBERIA',
		'LIBYA',
		'LIECHTENSTEIN',
		'LITHUANIA',
		'LUXEMBOURG',
		'MACAU',
		'MADAGASCAR',
		'MALAWI',
		'MALAYSIA',
		'MALDIVES',
		'MALI',
		'MALTA',
		'MARSHALL_ISLANDS',
		'MARTINIQUE',
		'MAURITANIA',
		'MAURITIUS',
		'MAYOTTE',
		'MEXICO',
		'MICRONESIA',
		'MOLDOVA',
		'MONACO',
		'MONGOLIA',
		'MONTENEGRO',
		'MONTSERRAT',
		'MOROCCO',
		'MOZAMBIQUE',
		'NAMIBIA',
		'NAURU',
		'NEPAL',
		'NETHERLANDS',
		'NEW_CALEDONIA',
		'NEW_ZEALAND',
		'NICARAGUA',
		'NIGER',
		'NIGERIA',
		'NIUE',
		'NORTH_MACEDONIA',
		'NORWAY',
		'OMAN',
		'OTHER_FOREIGN_LOCALITIES',
		'PAKISTAN',
		'PALAU',
		'PANAMA',
		'PAPUA_NEW_GUINEA',
		'PARAGUAY',
		'PERU',
		'PHILIPPINES',
		'POLAND',
		'PORTUGAL',
		'QATAR',
		'REPUBLIC_OF_THE_CONGO',
		'REUNION',
		'ROMANIA',
		'RUSSIA',
		'RWANDA',
		'SAINT_HELENA',
		'SAINT_KITTS_AND_NEVIS',
		'SAINT_VINCENT_AND_GRENADINES',
		'SAMOA',
		'SAN_MARINO',
		'SAO_TOME_AND_PRINCIPE',
		'SAUDI_ARABIA',
		'SENEGAL',
		'SERBIA',
		'SEYCHELLES',
		'SIERRA_LEONE',
		'SINGAPORE',
		'SINT_MAARTEN',
		'SLOVAKIA',
		'SLOVENIA',
		'SOLOMON_ISLANDS',
		'SOMALIA',
		'SOUTH_AFRICA',
		'SOUTH_SUDAN',
		'SPAIN',
		'SRI_LANKA',
		'ST_LUCIA',
		'SUDAN',
		'SURINAME',
		'SWEDEN',
		'SWITZERLAND',
		'SYRIA',
		'TAIWAN',
		'TAJIKISTAN',
		'TANZANIA',
		'THAILAND',
		'TIMOR_LESTE',
		'TOGO',
		'TOKELAU',
		'TONGA',
		'TRINIDAD_AND_TOBAGO',
		'TUNISIA',
		'TURKEY',
		'TURKMENISTAN',
		'TURKS_AND_CAICOS_ISLANDS',
		'TUVALU',
		'UGANDA',
		'UKRAINE',
		'UNITED_ARAB_EMIRATES',
		'UNITED_KINGDOM',
		'URUGUAY',
		'UZBEKISTAN',
		'VANUATU',
		'VENEZUELA',
		'VIETNAM',
		'VIRGIN_ISLANDS_BRITISH',
		'WALLIS_AND_FUTUNA',
		'YEMEN',
		'ZAMBIA',
		'ZIMBABWE'
	];

	function addStay() {
		if (!tempStay.location.city || tempStay.days < 1) return;

		const newStay: StayModelType = {
			days: tempStay.days,
			location:
				tempStay.location.kind === 'us'
					? {
							kind: 'us',
							country: 'UNITED_STATES',
							state: tempStay.location.state!,
							city: tempStay.location.city
						}
					: {
							kind: 'foreign',
							country: tempStay.location.country,
							city: tempStay.location.city
						},
			is_first_travel_day: tempStay.is_first_travel_day,
			is_last_travel_day: tempStay.is_last_travel_day,
			deduct_meals: tempStay.deduct_meals
		};

		stays = [...stays, newStay];

		// Reset form
		tempStay = {
			days: 1,
			location: {
				kind: 'us',
				country: 'UNITED_STATES',
				state: 'CA',
				city: ''
			},
			is_first_travel_day: false,
			is_last_travel_day: false,
			deduct_meals: false
		};
	}

	function removeStay(idx: number) {
		stays = stays.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await findMealAndLodgingApiEstimatesPerDiemPost({
				body: { stays }
			});
		} catch (e: any) {
			errorMsg = e?.message ?? 'Something went wrong fetching per-diem estimates.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="mx-auto max-w-3xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Per-Diem Estimates</h1>
		<div class="text-sm text-gray-500">Meal & Lodging Calculator</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add stay location</h2>

		<div class="space-y-4">
			<div class="flex gap-4">
				<label class="inline-flex items-center gap-2">
					<input type="radio" bind:group={tempStay.location.kind} value="us" class="text-black" />
					<span>US Location</span>
				</label>
				<label class="inline-flex items-center gap-2">
					<input
						type="radio"
						bind:group={tempStay.location.kind}
						value="foreign"
						class="text-black"
					/>
					<span>Foreign Location</span>
				</label>
			</div>

			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium">
					Days
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="1"
						bind:value={tempStay.days}
					/>
				</label>

				<label class="block text-sm font-medium">
					City
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="text"
						bind:value={tempStay.location.city}
						placeholder="e.g. San Francisco"
					/>
				</label>

				{#if tempStay.location.kind === 'us'}
					<label class="block text-sm font-medium">
						State
						<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempStay.location.state}>
							{#each US_STATES as state}
								<option value={state}>{state}</option>
							{/each}
						</select>
					</label>
				{:else}
					<label class="block text-sm font-medium">
						Country
						<select
							class="mt-1 w-full rounded-xl border p-2"
							bind:value={tempStay.location.country}
						>
							{#each ALL_COUNTRIES as country}
								<option value={country}>{country.replace(/_/g, ' ')}</option>
							{/each}
						</select>
					</label>
				{/if}
			</div>

			<div class="flex gap-4">
				<label class="inline-flex items-center gap-2">
					<input type="checkbox" bind:checked={tempStay.is_first_travel_day} class="rounded" />
					<span class="text-sm">First travel day</span>
				</label>
				<label class="inline-flex items-center gap-2">
					<input type="checkbox" bind:checked={tempStay.is_last_travel_day} class="rounded" />
					<span class="text-sm">Last travel day</span>
				</label>
				<label class="inline-flex items-center gap-2">
					<input type="checkbox" bind:checked={tempStay.deduct_meals} class="rounded" />
					<span class="text-sm">Deduct meals</span>
				</label>
			</div>
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addStay}
				disabled={!tempStay.location.city || tempStay.days < 1}
			>
				Add stay
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (stays = [])}
				disabled={!stays.length}
			>
				Clear all
			</button>
		</div>

		{#if stays.length}
			<ul class="divide-y rounded-xl border">
				{#each stays as stay, i}
					<li class="flex items-center justify-between p-3">
						<div class="text-sm">
							<div class="font-medium">
								{stay.location.city}
								{#if stay.location.kind === 'us' && 'state' in stay.location}
									, {stay.location.state}
								{:else if stay.location.kind === 'foreign' && 'country' in stay.location}
									, {stay.location.country}
								{/if}
							</div>
							<div class="text-gray-500">
								{stay.days} day{stay.days !== 1 ? 's' : ''}
								{#if stay.is_first_travel_day || stay.is_last_travel_day}
									•
									{#if stay.is_first_travel_day}First day{/if}
									{#if stay.is_first_travel_day && stay.is_last_travel_day}
										&
									{/if}
									{#if stay.is_last_travel_day}Last day{/if}
								{/if}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeStay(i)}>
							Remove
						</button>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No stays added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!stays.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Calculate per-diem
				{/if}
			</button>
			<span class="text-sm text-gray-500">
				{!stays.length ? 'Add at least one stay' : ''}
			</span>
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
