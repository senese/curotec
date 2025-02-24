export default interface IOrder {
  id: string;
  name: string;
  value: number;
};

export default class Order implements IOrder {
  constructor (order: IOrder) {
      this.id = order.id
      this.name = order.name
      this.value = order.value
  }
}