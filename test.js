export default {
  template: `
    <div>
      <button @click="runTest">Run Test</button>
      <button @click="calculate">Calculate Sum</button>
    </div>
  `,
  meta: {
    title: 'Dynamic Component from Github',
    route: '/dynamic-gtb',
  },
  inject: ['util'],
  methods: {
    runTest() {
      this.util.test();
    },
    calculate() {
      const result = this.util.calculateSum(3, 5);
      console.log('Sum result:', result);
    },
  },
};
