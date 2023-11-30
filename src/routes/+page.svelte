<script lang="ts">
  let isLoading = false;
  let files: FileList;

  async function uploadFile() {
    isLoading = true;
    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const fileUrl = await response.text();
        window.location.href = fileUrl;
      } else {
        console.error("File upload failed");
      }
    } catch (error) {
      console.error("An error occurred:", error);
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="bg-slate-500 text-black flex justify-center items-center h-screen">
  <form
    id="uploadForm"
    class="text-center"
    method="post"
    on:submit|preventDefault={uploadFile}
  >
    <input type="file" id="mp3File" accept=".mp3" bind:files />
    <button
      type="submit"
      class="bg-white uppercase rounded p-3 mt-4"
      disabled={isLoading}
    >
      Upload!
    </button>
  </form>
</main>
