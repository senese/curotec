export default interface IOrder {
  id: number;
  name: string;
  value: number;
  user_id?: number;
};

export default class Order implements IOrder {
  constructor (order: IOrder) {
      this.id = order.id
      this.name = order.name
      this.value = order.value
      this.user_id = order.user_id
  }
}