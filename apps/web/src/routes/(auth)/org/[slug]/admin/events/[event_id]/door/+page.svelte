<script lang="ts">
	import { resolve } from '$app/paths';
	import { Camera, CameraOff, ArrowLeft } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import QrCameraScanner from '$lib/components/tickets/QrCameraScanner.svelte';
	import CheckInDialog from '$lib/components/tickets/CheckInDialog.svelte';
	import MemberScanResultDialog from '$lib/components/members/MemberScanResultDialog.svelte';
	import { createTicketScanCheckIn } from '$lib/components/tickets/ticket-scan-checkin.svelte';
	import { needsPaymentConfirmation } from '$lib/utils/ticket-helpers';
	import { authStore } from '$lib/stores/auth.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';
	const { data }: { data: PageData } = $props();
	let camera = $state(false);
	const scan = createTicketScanCheckIn({
		getEventId: () => data.event.id,
		getAccessToken: () => authStore.accessToken
	});
	async function handleScan(code: string) {
		camera = false;
		await scan.handleQRScan(code);
	}
</script>

<svelte:head><title>{m['workspace.door']()} · {data.event.name}</title></svelte:head>
<div class="mx-auto max-w-3xl space-y-8">
	<a
		class="inline-flex items-center gap-2 text-sm text-muted-foreground"
		href={resolve('/(auth)/org/[slug]/admin', { slug: data.event.organization_slug })}
		><ArrowLeft size={16} />{m['workspace.eventsRecent']()}</a
	>
	<PageHeader title={m['workspace.door']()} subtitle={data.event.name} />
	<div class="flex flex-wrap gap-x-8 gap-y-3 border-y py-5 text-sm">
		<span>{m['workspace.issued']()}: <strong>{data.event.issued}</strong></span><span
			>{m['workspace.admissions']()}: <strong>{data.event.admissions}</strong></span
		>
	</div>
	<p class="text-sm leading-relaxed text-muted-foreground">{m['qrScannerModal.instructions']()}</p>
	<Button variant={camera ? 'outline' : 'default'} onclick={() => (camera = !camera)}
		>{#if camera}<CameraOff size={18} />{m['qrScannerModal.cancel']()}{:else}<Camera size={18} />{m[
				'eventTicketsAdmin.scanQRButton'
			]()}{/if}</Button
	>
	<QrCameraScanner active={camera} onScan={handleScan} />
	<p class="border-t pt-5 text-xs leading-relaxed text-muted-foreground">
		{m['workspace.reservationNote']()}
	</p>
</div>
<CheckInDialog
	isOpen={scan.showCheckInDialog}
	ticket={scan.ticketToCheckIn}
	needsPaymentConfirmation={scan.ticketToCheckIn
		? needsPaymentConfirmation(scan.ticketToCheckIn)
		: false}
	onConfirm={scan.submitCheckIn}
	onCancel={scan.closeCheckIn}
	isLoading={scan.checkInPending}
	errorMessage={scan.checkInDialogError}
/>
<MemberScanResultDialog
	report={scan.memberReport}
	pendingTicketId={scan.pendingMemberTicketId}
	onCheckInTicket={scan.checkInMemberTicket}
	onClose={scan.closeMemberReport}
/>
