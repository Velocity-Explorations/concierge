<script lang="ts">
	import { client } from '../../client/client.gen';
	import { translateTextsApiEstimatesTranslationsPost } from '../../client/sdk.gen';
	import type { TranslationModel, InterpretationModel, LanguageName } from '../../client/types.gen';

	client.setConfig({ baseUrl: 'http://localhost:8000' });

	type JobType = TranslationModel | InterpretationModel;
	type JobKind = 'translation' | 'interpretation';

	const LANGUAGES: LanguageName[] = [
		'ENGLISH',
		'SPANISH',
		'FRENCH',
		'PORTUGUESE',
		'ITALIAN',
		'GERMAN',
		'DUTCH',
		'CHINESE',
		'VIETNAMESE',
		'HINDI',
		'BENGALI',
		'POLISH',
		'SWEDISH',
		'ARABIC',
		'RUSSIAN',
		'UKRAINIAN',
		'ROMANIAN',
		'TURKISH',
		'KOREAN',
		'JAPANESE',
		'THAI',
		'GREEK',
		'HEBREW',
		'PERSIAN',
		'CZECH',
		'SLOVAK',
		'HUNGARIAN',
		'LITHUANIAN',
		'LATVIAN',
		'ESTONIAN',
		'DANISH',
		'NORWEGIAN',
		'FINNISH',
		'MALAY',
		'INDONESIAN',
		'TAGALOG',
		'SERBIAN',
		'CROATIAN',
		'BOSNIAN',
		'BULGARIAN',
		'SLOVENIAN',
		'ALBANIAN',
		'GEORGIAN',
		'ARMENIAN',
		'AZERBAIJANI',
		'MONGOLIAN',
		'LAO',
		'KHMER',
		'AMHARIC',
		'TIGRINYA',
		'SOMALI',
		'ZULU',
		'XHOSA',
		'AFRIKAANS',
		'SWAHILI',
		'KINYARWANDA',
		'KIRUNDI',
		'WOLOF',
		'HAUSA',
		'YORUBA',
		'IGBO',
		'TWI',
		'LUXEMBOURGISH',
		'FAROESE',
		'ICELANDIC',
		'UZBEK',
		'TAJIK',
		'TURKMEN',
		'KYRGYZ',
		'KAZAKH',
		'PASHTO',
		'DARI',
		'NEPALI',
		'SINHALA',
		'TAMIL',
		'URDU',
		'MACEDONIAN',
		'BASQUE',
		'CATALAN',
		'GALICIAN',
		'BELARUSIAN',
		'TONGAN',
		'SAMOAN',
		'FIJIAN',
		'BISLAMA',
		'PALAUAN',
		'MARSHALLESE',
		'NAURUAN',
		'NIUEAN',
		'TOKELAUAN',
		'GREENLANDIC',
		'TAHITIAN',
		'REUNION_FRENCH',
		'MAYOTTE_FRENCH',
		'!KUNG'
	];

	const TRANSLATION_TYPES: TranslationModel['type'][] = ['Translation'];
	const TRANSLATION_UOMS: TranslationModel['uom'][] = [
		'Word',
		'Rush Rate (Word)',
		'Overtime Hour',
		'Page'
	];

	const INTERPRETATION_TYPES: InterpretationModel['type'][] = [
		'Interpretation',
		'Consecutive Interpretation',
		'Simultaneous Interpretation'
	];
	const INTERPRETATION_UOMS: InterpretationModel['uom'][] = ['Hour', 'Day', 'Half Day'];

	let jobs = $state<JobType[]>([]);

	let tempJob = $state<{
		kind: JobKind;
		src: LanguageName;
		target: LanguageName;
		type: TranslationModel['type'] | InterpretationModel['type'];
		uom: TranslationModel['uom'] | InterpretationModel['uom'];
		quantity: number;
	}>({
		kind: 'translation',
		src: 'ENGLISH',
		target: 'SPANISH',
		type: 'Translation',
		uom: 'Word',
		quantity: 100
	});

	let res: unknown = $state();
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	$effect(() => {
		if (tempJob.kind === 'translation') {
			tempJob.type = 'Translation';
			tempJob.uom = 'Word';
		} else {
			tempJob.type = 'Interpretation';
			tempJob.uom = 'Hour';
		}
	});

	function addJob() {
		if (!tempJob.src || !tempJob.target || !tempJob.type || !tempJob.uom || tempJob.quantity <= 0)
			return;

		const newJob: JobType =
			tempJob.kind === 'translation'
				? {
						src: tempJob.src,
						target: tempJob.target,
						type: tempJob.type as TranslationModel['type'],
						uom: tempJob.uom as TranslationModel['uom'],
						quantity: tempJob.quantity
					}
				: {
						src: tempJob.src,
						target: tempJob.target,
						type: tempJob.type as InterpretationModel['type'],
						uom: tempJob.uom as InterpretationModel['uom'],
						quantity: tempJob.quantity
					};

		jobs = [...jobs, newJob];

		tempJob = {
			kind: 'translation',
			src: 'ENGLISH',
			target: 'SPANISH',
			type: 'Translation',
			uom: 'Word',
			quantity: 100
		};
	}

	function removeJob(idx: number) {
		jobs = jobs.filter((_, i) => i !== idx);
	}

	async function submit() {
		loading = true;
		errorMsg = null;
		try {
			res = await translateTextsApiEstimatesTranslationsPost({
				body: { jobs }
			});
		} catch (e: unknown) {
			errorMsg = (e as Error)?.message ?? 'Something went wrong fetching translation estimates.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="mx-auto max-w-3xl space-y-6 p-6">
	<header class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold">Translation & Interpretation Estimates</h1>
		<div class="text-sm text-gray-500">Language Services Calculator</div>
	</header>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<h2 class="text-lg font-medium">Add translation/interpretation job</h2>

		<div class="space-y-4">
			<div class="flex gap-4">
				<label class="inline-flex items-center gap-2">
					<input type="radio" bind:group={tempJob.kind} value="translation" class="text-black" />
					<span>Translation</span>
				</label>
				<label class="inline-flex items-center gap-2">
					<input type="radio" bind:group={tempJob.kind} value="interpretation" class="text-black" />
					<span>Interpretation</span>
				</label>
			</div>

			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
				<label class="block text-sm font-medium">
					Source Language
					<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.src}>
						{#each LANGUAGES as language (language)}
							<option value={language}>{language.replace(/_/g, ' ')}</option>
						{/each}
					</select>
				</label>

				<label class="block text-sm font-medium">
					Target Language
					<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.target}>
						{#each LANGUAGES as language (language)}
							<option value={language}>{language.replace(/_/g, ' ')}</option>
						{/each}
					</select>
				</label>

				{#if tempJob.kind === 'translation'}
					<label class="block text-sm font-medium">
						Translation Type
						<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.type}>
							{#each TRANSLATION_TYPES as type (type)}
								<option value={type}>{type}</option>
							{/each}
						</select>
					</label>

					<label class="block text-sm font-medium">
						Unit of Measure
						<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.uom}>
							{#each TRANSLATION_UOMS as uom (uom)}
								<option value={uom}>{uom}</option>
							{/each}
						</select>
					</label>
				{:else}
					<label class="block text-sm font-medium">
						Interpretation Type
						<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.type}>
							{#each INTERPRETATION_TYPES as type (type)}
								<option value={type}>{type}</option>
							{/each}
						</select>
					</label>

					<label class="block text-sm font-medium">
						Unit of Measure
						<select class="mt-1 w-full rounded-xl border p-2" bind:value={tempJob.uom}>
							{#each INTERPRETATION_UOMS as uom (uom)}
								<option value={uom}>{uom}</option>
							{/each}
						</select>
					</label>
				{/if}

				<label class="block text-sm font-medium">
					Quantity
					<input
						class="mt-1 w-full rounded-xl border p-2"
						type="number"
						min="1"
						bind:value={tempJob.quantity}
					/>
				</label>
			</div>
		</div>

		<div class="flex gap-3">
			<button
				type="button"
				class="rounded-xl bg-black px-4 py-2 text-white disabled:opacity-50"
				onclick={addJob}
				disabled={!tempJob.src || !tempJob.target || tempJob.quantity <= 0}
			>
				Add job
			</button>
			<button
				type="button"
				class="rounded-xl border px-4 py-2"
				onclick={() => (jobs = [])}
				disabled={!jobs.length}
			>
				Clear all
			</button>
		</div>

		{#if jobs.length}
			<ul class="divide-y rounded-xl border">
				{#each jobs as job, i (i)}
					<li class="flex items-center justify-between p-3">
						<div class="text-sm">
							<div class="font-medium">
								{job.src.replace(/_/g, ' ')} → {job.target.replace(/_/g, ' ')}
							</div>
							<div class="text-gray-500">
								{job.type} • {job.quantity}
								{job.uom}{job.quantity !== 1 ? 's' : ''}
							</div>
						</div>
						<button class="rounded-lg border px-3 py-1 text-sm" onclick={() => removeJob(i)}>
							Remove
						</button>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-sm text-gray-500">No jobs added yet.</p>
		{/if}
	</section>

	<section class="space-y-4 rounded-2xl bg-white p-5 shadow">
		<div class="flex items-center gap-3">
			<button
				class="rounded-xl bg-black px-5 py-2.5 text-white disabled:opacity-50"
				onclick={submit}
				disabled={!jobs.length || loading}
			>
				{#if loading}
					<span class="animate-pulse">Fetching…</span>
				{:else}
					Get estimates
				{/if}
			</button>
			<span class="text-sm text-gray-500">
				{!jobs.length ? 'Add at least one job' : ''}
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
