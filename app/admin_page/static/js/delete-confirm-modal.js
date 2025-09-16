const DeleteConfirmModal = {
    template:  `
            <div id="delete-cf-modal" class="fixed top-0 left-0 right-0 z-[100] w-full h-full bg-black/60 flex items-center justify-center">
                <div class="rounded p-5 w-[600px] bg-white text-black">
                    <!-- Start Modal Head -->
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="text-md">Delete Confirmation</h3>
                        <button @click="onCloseModal">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <hr>
                    <!-- End Modal Head -->

                    <!-- Start Modal Body -->
                    <div class="mb-3 flex items-center gap-3 py-3">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-[100px]">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                        </svg>
                        <p class="text-xl mb-3">Are you sure to delete? it cannot undo.</p>
                    </div>
                   <!-- End Modal Body -->

                    <hr>
                    <!-- Start Modal Footer -->
                    <div class="mt-3 flex items-center justify-end gap-3">
                        <button class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded cursor-pointer" @click="onCloseModal">Cancel</button>
                        <button class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded cursor-pointer" @click="onDelete">Delete Now</button>
                    </div>
                    <!-- End Modal Footer -->
                </div>
            </div>
    `,
    methods: {
        onCloseModal() {
            this.$emit('on-close-modal');
        },
        onDelete(){
            this.$emit('on-delete')
        }
    }
}