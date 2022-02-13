<template>
  <div class="create-room-popup-bg">
    <div class="create-room-popup">
      <button @click="$emit('exit')">x</button>
      <h2>Create Room</h2>
      <form @submit.prevent="submitRoomForCreation">
        <div class="form-input-grouping">
          <label for="room-name">Room Name</label>
          <input id="room-name" type="text" placeholder="Enter room name..." v-model="roomName">
        </div>
        <div class="form-input-grouping">
          <label for="is-public">Public</label>
          <input id="id-public" type="checkbox" v-model="isPublic">
        </div>
        <div class="form-input-grouping" v-if="!isPublic">
          <label for="passcode">Passcode</label>
          <input id="passcode" type="password" placeholder="Enter passcode..." v-model="passcode">
        </div>
        <button type="submit">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreateRoomPopup',
  data: () => ({
    roomName: '',
    isPublic: true,
    passcode: ''
  }),
  methods: {
    submitRoomForCreation(){
      this.$emit('create', this.roomName, this.isPublic, this.passcode);
      this.$emit('exit');
    }
  }
}
</script>

<style>
  .create-room-popup-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    background-color: var(--surface1);
  }

  .create-room-popup {
    position: relative;
    padding: 1rem;
    color: var(--text2);
  }

  .create-room-popup > button {
    position: absolute;
    top: 0.2rem;
    right: 0.2rem;
  }

  .create-room-popup h2 {
    margin: 0;
    margin-bottom: 1rem;
    text-align: center;
  }

  .create-room-popup label {
    font-size: 1rem;
  }

  .create-room-popup input:not([type="checkbox"]) {
    display: block;
    background-color: var(--surface4);
    height: 2rem;
  }

  .create-room-popup label ~ input[type="checkbox"] {
    display: inline-block;
    margin: 0;
    margin-left: 1rem;
    padding: 0;
  }

  .form-input-grouping + .form-input-grouping {
    margin-top: 1rem;
  }

  .create-room-popup form button {
    display: block;
    margin: 0 auto;
    margin-top: 1rem;
    height: 30px;
    width: 200px;
  }
</style>