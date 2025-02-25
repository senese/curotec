import { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { useOrders } from "../contexts/OrderProvider";
import IOrder from "../types/order";
import toast, { Toaster } from "react-hot-toast";

interface EditModalProps {
  order: IOrder;
  showModal: boolean;
  setShowModal(): void;
}

function EditModal({ order, showModal, setShowModal }: EditModalProps) {
  const { updateOrder } = useOrders();
  const [name, setName] = useState(order.name);
  const [value, setValue] = useState(order.value);

  const handleNameChange = (e) => setName(e.target.value);
  const handleValueChange = (e) => setValue(e.target.value);
  const handleClose = () => setShowModal(false);
  const handleOrderUpdate = async () => {
    try {
      await updateOrder(order.id, name, value);
      handleClose();
      toast.success("Success")
    } catch {
      toast.error("Something went wrong")
    }
  };

  return (
    <>
      <div><Toaster/></div>
      <Modal show={showModal}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Order</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="name">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                value={name}
                onChange={handleNameChange}
                required
                autoFocus
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="value">
              <Form.Label>Value</Form.Label>
              <Form.Control
                type="number"
                value={value || ""}
                onChange={handleValueChange}
                required
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => handleClose()}>
            Close
          </Button>
          <Button variant="primary" onClick={() => handleOrderUpdate()}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default EditModal;
